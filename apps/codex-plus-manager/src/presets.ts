/**
 * Codex++ 供应商预设
 * 基于 cc-switch (MIT) 的 codexProviderPresets.ts，作者 Jason Young
 * https://github.com/farion1231/cc-switch
 *
 * 提供一键填充供应商配置的预设模板，包括 Base URL、协议、模型列表等。
 * 内置常用模型服务的官方与功能性预设。
 */

export type PresetCategory = "official" | "third_party" | "cn_official";

export type RelayProtocol = "responses" | "chatCompletions";

export interface ProviderPreset {
  id: string;
  name: string;
  category: PresetCategory;
  baseUrl: string;
  protocol: RelayProtocol;
  model: string;
  modelList?: string[];
}

/**
 * 预设列表。选择任一预设会自动填充：
 * - name     → 供应商名称
 * - baseUrl  → API 端点
 * - protocol → responses / chatCompletions（根据上游实际协议）
 * - model    → 默认模型名
 * - modelList → 可选模型清单（换行分隔）
 */
export const PRESETS: ProviderPreset[] = [
  // ── 官方 ──
  {
    id: "openai",
    name: "OpenAI Official",
    category: "official",
    baseUrl: "https://api.openai.com/v1",
    protocol: "responses",
    model: "gpt-5.5",
  },

  // ── 中国官方 ──
  {
    id: "deepseek",
    name: "DeepSeek",
    category: "cn_official",
    baseUrl: "https://api.deepseek.com",
    protocol: "chatCompletions",
    model: "deepseek-v4-flash",
    modelList: ["deepseek-v4-flash", "deepseek-v4-pro"],
  },
  {
    id: "zhipu-glm",
    name: "Zhipu GLM",
    category: "cn_official",
    baseUrl: "https://open.bigmodel.cn/api/coding/paas/v4",
    protocol: "chatCompletions",
    model: "glm-5.1",
    modelList: ["glm-5.1"],
  },
  {
    id: "kimi",
    name: "Kimi",
    category: "cn_official",
    baseUrl: "https://api.moonshot.cn/v1",
    protocol: "chatCompletions",
    model: "kimi-k2.6",
    modelList: ["kimi-k2.6"],
  },
  {
    id: "bailian",
    name: "Bailian (Qwen)",
    category: "cn_official",
    baseUrl: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    protocol: "chatCompletions",
    model: "qwen3-coder-plus",
    modelList: ["qwen3-coder-plus", "qwen3-max"],
  },
  {
    id: "stepfun",
    name: "StepFun",
    category: "cn_official",
    baseUrl: "https://api.stepfun.com/step_plan/v1",
    protocol: "chatCompletions",
    model: "step-3.5-flash-2603",
    modelList: ["step-3.5-flash-2603", "step-3.5-flash"],
  },
  {
    id: "minimax",
    name: "MiniMax",
    category: "cn_official",
    baseUrl: "https://api.minimaxi.com/v1",
    protocol: "chatCompletions",
    model: "MiniMax-M2.7",
    modelList: ["MiniMax-M2.7"],
  },
  {
    id: "volcano-ark",
    name: "火山引擎 Ark",
    category: "cn_official",
    baseUrl: "https://ark.cn-beijing.volces.com/api/coding/v3",
    protocol: "chatCompletions",
    model: "ark-code-latest",
    modelList: ["ark-code-latest"],
  },
  {
    id: "baidu-qianfan",
    name: "百度千帆 Coding Plan",
    category: "cn_official",
    baseUrl: "https://qianfan.baidubce.com/v2/coding",
    protocol: "chatCompletions",
    model: "qianfan-code-latest",
  },
  {
    id: "xiaomi-mimo",
    name: "小米 MiMo",
    category: "cn_official",
    baseUrl: "https://api.xiaomimimo.com/v1",
    protocol: "chatCompletions",
    model: "mimo-v2.5-pro",
    modelList: ["mimo-v2.5-pro"],
  },
  {
    id: "modelscope",
    name: "ModelScope",
    category: "cn_official",
    baseUrl: "https://api-inference.modelscope.cn/v1",
    protocol: "chatCompletions",
    model: "ZhipuAI/GLM-5.1",
    modelList: ["ZhipuAI/GLM-5.1"],
  },
  {
    id: "longcat",
    name: "Longcat",
    category: "cn_official",
    baseUrl: "https://api.longcat.chat/openai/v1",
    protocol: "chatCompletions",
    model: "LongCat-Flash-Chat",
    modelList: ["LongCat-Flash-Chat"],
  },

  // ── 第三方 ──
  {
    id: "azure",
    name: "Azure OpenAI",
    category: "third_party",
    baseUrl: "https://YOUR_RESOURCE_NAME.openai.azure.com/openai",
    protocol: "responses",
    model: "gpt-5.5",
  },
];
