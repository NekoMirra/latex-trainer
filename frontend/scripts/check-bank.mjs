// 题库自检脚本 - 校验 data/latex_bank.json 或单个课程片段
// 用法：node scripts/check-bank.mjs [课程片段文件...]
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import katex from 'katex';
import { checkAdvancedAnswerEquivalence } from '../src/utils/answerValidation.js';

const here = path.dirname(fileURLToPath(import.meta.url));
const BANK_PATH = path.resolve(here, '../../data/latex_bank.json');

const LANGUAGES = ['zh-CN', 'en-US'];
const DIFFICULTIES = ['easy', 'medium', 'hard'];
const LESSON_COUNT = 18;
const PRACTICES_PER_LESSON = 12;
const TOTAL_PRACTICES = LESSON_COUNT * PRACTICES_PER_LESSON;

const failures = [];
const log = console.log.bind(console);
// 判分函数内部有大量调试输出，自检期间静音
console.log = () => {};

const fail = (message) => failures.push(message);
const isFilled = (value) => typeof value === 'string' && value.trim().length > 0;
const squeeze = (value) => value.replace(/\s+/g, ' ').trim();

const sameKeys = (object, expected) => {
  if (object === null || typeof object !== 'object') return false;
  const keys = Object.keys(object).sort();
  const wanted = [...expected].sort();
  return keys.length === wanted.length && keys.every((key, index) => key === wanted[index]);
};

const collectMathSegments = (text) => {
  const segments = [];
  const withoutDisplay = text.replace(/\$\$([\s\S]+?)\$\$/g, (_match, body) => {
    segments.push(body);
    return ' ';
  });
  withoutDisplay.replace(/\$([^$\n]+?)\$/g, (_match, body) => {
    segments.push(body);
    return ' ';
  });
  return segments;
};

const checkKatex = (expression, label) => {
  try {
    katex.renderToString(expression, { throwOnError: true, displayMode: false });
  } catch (error) {
    fail(`${label}: KaTeX 渲染失败 ${JSON.stringify(expression)} → ${error.message}`);
  }
};

const scriptVariants = (formula) => [
  formula,
  formula.replace(/\s+/g, ''),
  formula.replace(/\^([A-Za-z0-9])/g, '^{$1}').replace(/_([A-Za-z0-9])/g, '_{$1}')
];

const gradingCases = [];

const validateLesson = (lesson) => {
  const lessonTag = `第${lesson?.sequence}课`;

  if (!Number.isInteger(lesson?.sequence)) fail(`${lessonTag}: sequence 必须是整数`);
  for (const language of LANGUAGES) {
    if (!isFilled(lesson?.title?.[language])) fail(`${lessonTag}: title.${language} 为空`);
    if (!isFilled(lesson?.description?.[language])) fail(`${lessonTag}: description.${language} 为空`);
  }
  if (!sameKeys(lesson?.title, LANGUAGES)) fail(`${lessonTag}: title 语言键集合应为 ${LANGUAGES.join('/')}`);
  if (!sameKeys(lesson?.description, LANGUAGES)) fail(`${lessonTag}: description 语言键集合应为 ${LANGUAGES.join('/')}`);

  if (!Array.isArray(lesson?.cards) || lesson.cards.length === 0) {
    fail(`${lessonTag}: cards 为空`);
    return null;
  }

  let practiceCount = 0;
  const knowledgeCountExisting = lesson.cards.filter((card) => card.type === 'knowledge').length;
  const difficulties = { easy: 0, medium: 0, hard: 0 };
  const questions = new Set();
  const formulas = new Set();

  lesson.cards.forEach((card, index) => {
    const cardTag = `${lessonTag} 第${index}张卡`;

    if (card.type === 'knowledge') {
      if (!sameKeys(card.content, LANGUAGES)) fail(`${cardTag}: content 语言键集合应为 ${LANGUAGES.join('/')}`);
      for (const language of LANGUAGES) {
        const content = card.content?.[language];
        if (!isFilled(content)) {
          fail(`${cardTag}: content.${language} 为空`);
          continue;
        }
        const segments = collectMathSegments(content);
        if (segments.length === 0) fail(`${cardTag}: content.${language} 没有 $...$ 公式示例`);
        segments.forEach((segment) => checkKatex(segment, `${cardTag} content.${language}`));
      }
      return;
    }

    if (card.type !== 'practice') {
      fail(`${cardTag}: 未知卡片类型 ${JSON.stringify(card.type)}`);
      return;
    }

    practiceCount += 1;
    if (!sameKeys(card.question, LANGUAGES)) fail(`${cardTag}: question 语言键集合应为 ${LANGUAGES.join('/')}`);
    if (!sameKeys(card.hints, LANGUAGES)) fail(`${cardTag}: hints 语言键集合应为 ${LANGUAGES.join('/')}`);

    for (const language of LANGUAGES) {
      if (!isFilled(card.question?.[language])) fail(`${cardTag}: question.${language} 为空`);
      const hints = card.hints?.[language];
      if (!Array.isArray(hints) || hints.length < 2 || hints.length > 4) {
        fail(`${cardTag}: hints.${language} 应为 2-4 条，实际 ${Array.isArray(hints) ? hints.length : '非数组'}`);
        continue;
      }
      hints.forEach((hint, hintIndex) => {
        if (!isFilled(hint)) fail(`${cardTag}: hints.${language}[${hintIndex}] 为空`);
      });
    }

    if (!DIFFICULTIES.includes(card.difficulty)) {
      fail(`${cardTag}: difficulty 非法 ${JSON.stringify(card.difficulty)}`);
    } else {
      difficulties[card.difficulty] += 1;
    }

    const formula = card.target_formula;
    if (!isFilled(formula)) {
      fail(`${cardTag}: target_formula 为空`);
      return;
    }
    const trimmed = formula.trim();
    if (!/^\$\$[\s\S]*\$\$$/.test(trimmed) && !/^\$[\s\S]*\$$/.test(trimmed)) {
      fail(`${cardTag}: target_formula 未被 $...$ 包裹 ${JSON.stringify(formula)}`);
    }
    const body = trimmed.replace(/^\$\$|\$\$$/g, '').replace(/^\$|\$$/g, '');
    checkKatex(body, `${cardTag} target_formula`);

    const questionText = squeeze(card.question?.['zh-CN'] ?? '');
    const formulaText = squeeze(trimmed);
    if (questions.has(questionText)) fail(`${cardTag}: 课内题干重复 ${JSON.stringify(questionText)}`);
    if (formulas.has(formulaText)) fail(`${cardTag}: 课内 target_formula 重复 ${JSON.stringify(formulaText)}`);
    questions.add(questionText);
    formulas.add(formulaText);

    gradingCases.push({ label: cardTag, formula: trimmed });
  });

  if (practiceCount !== PRACTICES_PER_LESSON) {
    fail(`${lessonTag}: 练习题应为 ${PRACTICES_PER_LESSON} 道，实际 ${practiceCount} 道`);
  }
  if (difficulties.easy < 3) fail(`${lessonTag}: easy 题不足 3 道（实际 ${difficulties.easy}）`);
  if (difficulties.medium < 5) fail(`${lessonTag}: medium 题不足 5 道（实际 ${difficulties.medium}）`);

  return { sequence: lesson.sequence, practiceCount, knowledgeCount: knowledgeCountExisting, difficulties };
};

const fragmentPaths = process.argv.slice(2);
const distribution = [];
let totalPractices = 0;

if (fragmentPaths.length > 0) {
  for (const fragmentPath of fragmentPaths) {
    const lesson = JSON.parse(readFileSync(fragmentPath, 'utf8'));
    const row = validateLesson(lesson);
    if (row) {
      distribution.push({ ...row, file: path.basename(fragmentPath) });
      totalPractices += row.practiceCount;
    }
  }
} else {
  const bank = JSON.parse(readFileSync(BANK_PATH, 'utf8'));
  if (bank.version !== 1) fail(`version 应为 1，实际为 ${JSON.stringify(bank.version)}`);
  if (!Array.isArray(bank.lessons)) {
    fail('lessons 必须是数组');
  } else {
    if (bank.lessons.length !== LESSON_COUNT) fail(`课程数应为 ${LESSON_COUNT}，实际为 ${bank.lessons.length}`);
    const sequences = bank.lessons.map((lesson) => lesson.sequence);
    if (new Set(sequences).size !== sequences.length) fail('sequence 存在重复');
    for (let expected = 1; expected <= LESSON_COUNT; expected += 1) {
      if (!sequences.includes(expected)) fail(`缺少 sequence=${expected} 的课程`);
    }
    for (const lesson of bank.lessons) {
      const row = validateLesson(lesson);
      if (row) {
        distribution.push({ ...row, file: BANK_PATH });
        totalPractices += row.practiceCount;
      }
    }
    if (totalPractices !== TOTAL_PRACTICES) {
      fail(`练习题总数应为 ${TOTAL_PRACTICES}，实际为 ${totalPractices}`);
    }
  }
}

// 判分闭环
for (const { label, formula } of gradingCases) {
  for (const variant of scriptVariants(formula)) {
    const result = await checkAdvancedAnswerEquivalence(variant, formula);
    if (!result.isCorrect) fail(`${label}: 正确答案变体被判错 ${JSON.stringify(variant)} vs ${JSON.stringify(formula)}`);
  }
  const negative = await checkAdvancedAnswerEquivalence('\\text{WRONG}', formula);
  if (negative.isCorrect) fail(`${label}: 错误答案被判对 \\text{WRONG} vs ${JSON.stringify(formula)}`);
}

console.log = log;
for (const row of distribution) {
  log(`  第${String(row.sequence).padStart(2, '0')}课 练习 ${row.practiceCount} | 知识点 ${row.knowledgeCount} | easy ${row.difficulties.easy} | medium ${row.difficulties.medium} | hard ${row.difficulties.hard}`);
}

if (failures.length > 0) {
  log(`\n自检失败 ${failures.length} 项：`);
  failures.forEach((message) => log(`  ✗ ${message}`));
  process.exitCode = 1;
} else if (fragmentPaths.length > 0) {
  log(`\n${distribution.length} 个课程片段 / ${totalPractices} 道练习 / katex ok / grading ok`);
} else {
  log(`\n${LESSON_COUNT} lessons / ${totalPractices} practices / katex ok / grading ok`);
}