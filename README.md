# Sunyu Baobao · Codex 桌宠素材库

这是「Sunyu Baobao」Codex 桌宠的版本化素材仓库，而不是一个独立运行的应用。每个版本包含可安装的宠物清单 `pet.json`、精灵图 `spritesheet.webp`，以及相应的验收记录、预览或制作资料。

> **许可与商用限制：**本仓库公开源代码和素材，但全部内容仅允许个人非商业使用。**未经书面授权，严禁任何形式的商业使用。**合作请通过 [GitHub Issues](https://github.com/Fingxing2025/sunyubao-project/issues) 联系，完整条款见 [LICENSE](LICENSE) 和 [ASSET_LICENSE.md](ASSET_LICENSE.md)。

## 当前状态

当前推荐使用 `codex-pet-foot-forward` 中的 **夸张赤脚前伸版（内侧大拇趾修正）**：

- 安装包：`Sunyu-Baobao-夸张赤脚前伸版-内侧大拇趾修正.zip`
- 宠物 ID：`sunyu-baobao`
- 图集规范：Codex v1，`1536 × 1872`，`9 × 8` 格
- 更新范围：只替换 `running-right` 与 `running-left` 两个方向动作；其余 7 个动作保留自 `codex-pet-run-dynamics`
- 内容：坐姿抱臂、赤脚脚底朝镜头前伸/回收；左右方向按镜像处理，两个大拇趾均位于画面内侧

本工作区中的已安装副本与该版本的 `final/spritesheet.webp` 哈希一致。图集结构校验与逐帧人工复核均通过，详细证据见：

- `codex-pet-foot-forward/final/validation.json`
- `codex-pet-foot-forward/qa/run-summary-final.json`
- `codex-pet-foot-forward/qa/contact-sheet-inner-toe.png`

> 边界说明：最新版本的本地预览服务已返回 HTTP 200，但最后一次 Playwright 点击/截图没有完成，因此不把它表述为最终的浏览器交互验收。Codex 原生窗口仍需要在本机刷新列表、重新选择宠物后由使用者确认。

## 安装推荐版

先解压 `codex-pet-foot-forward/Sunyu-Baobao-夸张赤脚前伸版-内侧大拇趾修正.zip`，其中会得到 `sunyu-baobao/` 文件夹。

1. 如已安装同名桌宠，先把现有 `sunyu-baobao` 文件夹改名或复制到安全位置备份。
2. 将解压出的 `sunyu-baobao/` 放到下列宠物目录：

   | 系统 | 目标目录 |
   | --- | --- |
   | macOS / Linux | `~/.codex/pets/sunyu-baobao/` |
   | Windows | `%USERPROFILE%\.codex\pets\sunyu-baobao\` |

3. 在 Codex 的设置中刷新宠物/Mini 列表，重新选择「Sunyu Baobao」；如未加载，重启 Codex 后再次选择。

macOS / Linux 示例（这些命令会创建目标目录并覆盖同名的两个资源文件；执行前请完成第 1 步备份）：

```bash
unzip "codex-pet-foot-forward/Sunyu-Baobao-夸张赤脚前伸版-内侧大拇趾修正.zip" -d /tmp/sunyu-baobao-install
mkdir -p "$HOME/.codex/pets/sunyu-baobao"
cp /tmp/sunyu-baobao-install/sunyu-baobao/pet.json "$HOME/.codex/pets/sunyu-baobao/"
cp /tmp/sunyu-baobao-install/sunyu-baobao/spritesheet.webp "$HOME/.codex/pets/sunyu-baobao/"
```

命令的关键结果是目标目录中同时存在 `pet.json` 和 `spritesheet.webp`；它不会自动刷新 Codex 的宠物列表。

## 版本一览

| 目录 | 定位 | 交付状态 |
| --- | --- | --- |
| `codex-pet` | 原始基础版 | 可安装基线与完整的 9 状态预览记录 |
| `codex-pet-smooth` | 自然动作调整 | 保持原生节奏，替换部分动作以减小姿态跳变 |
| `codex-pet-gait-fix` | 手脚交替修复 | 修复两个方向小跑的支撑与交替关系 |
| `codex-pet-fluid` | 关节补间小跑 | 对方向小跑行进行程序化关节插值 |
| `codex-pet-wide-gait` | 大步幅实验版 | 仅更新两个方向小跑行；与后续动态版并列保留作对照 |
| `codex-pet-run-dynamics` | 动态跑步基线 | 大跨步、后脚腾空、反向摆臂；是当前推荐版其余 7 个动作的来源 |
| `codex-pet-foot-forward` | **当前推荐版** | 两个方向动作改为赤脚脚底前伸，已生成最终安装包与验收材料 |

除推荐版外，其余目录主要用于回退、对照和复现；不要依据目录名称推断它们是当前默认安装版本。

## 目录约定

一个可交付版本通常具有以下结构：

```text
codex-pet-<version>/
├── final/                 # 最终 pet.json、spritesheet.webp 与结构校验
├── qa/                    # 验收摘要、逐帧检查、接触表、预览结果
├── backup-installed*/     # 安装前或旧版本备份（若该版本有）
├── frames/ / decoded/     # 可复现的中间帧（若该版本有）
├── prompts/ / scripts/    # 生成提示词与组装、校验脚本（若该版本有）
├── 使用说明.md             # 该版本的具体动作与安装说明
└── *.zip                  # 可安装包（若已打包）
```

`final/` 是该版本的资源真源；`qa/` 用于说明它经过了哪些检查，不应被当作运行时依赖。不同历史版本中可能有同名压缩包，安装前务必以所在目录和 `使用说明.md` 为准。

## 预览、校验与继续开发

- 可直接打开版本目录内的 HTML 预览文件，例如 `codex-pet-foot-forward/桌宠预览.html`。它适合查看动作，不等同于 Codex 原生窗口的最终验收。
- 校验结论以各版本的 `final/validation.json` 与 `qa/run-summary.json`（推荐版为 `qa/run-summary-final.json`）为准。
- 修改精灵图时，请只在一个版本目录内工作，保留已有备份与未修改动作行，并重新生成 `final/`、安装包及验收记录。
- 仓库根目录提供 `install-to-codex.sh`（macOS/Linux）和 `install-to-codex.ps1`（Windows）。脚本会先备份同名旧桌宠，再只安装 `pet.json` 与 `spritesheet.webp`；也可以继续使用上方的手动解压/复制流程。

## 协作注意事项

- 大部分成果为图片和压缩包等二进制文件；不要无意转码或批量重压缩。
- 当前工作区包含尚未提交的较新版本和验收材料。推送前请先检查版本目录、安装包和 README 是否在同一次提交中，避免远程仓库只有说明而缺少对应资源。
- 任何“已安装”或“可选中”的结论都应区分资源哈希、浏览器预览和 Codex 原生窗口三种验证层级。

## 许可、AI 与品牌声明

- Python、Shell、PowerShell、HTML、文档和配置等代码内容同样仅限个人非商业使用；本项目不采用允许商用的 MIT、Apache 或 GPL 等开源许可证。完整条款见 [LICENSE](LICENSE)。
- JPG、PNG、WebP、GIF、压缩包、嵌入 HTML 的人物图像，以及可识别的「Sunyu Baobao」角色形象，仅允许个人非商业使用；未经书面授权，严禁任何形式的商用、转售、再许可、广告代言、身份冒充、人脸识别或 AI 训练。完整条款见 [ASSET_LICENSE.md](ASSET_LICENSE.md)。
- 本项目的部分角色图像和动画由 AI 工具辅助生成或编辑，并经人工筛选、组装和校验。转载或发布相关素材时，应保留 AI 生成说明及依法、依平台规则需要保留的标识。
- 本项目是独立的非官方社区项目，与 OpenAI 不存在隶属、赞助或背书关系。OpenAI、Codex 及相关标识归其各自权利人所有。
- 合作、媒体使用或其他授权咨询，请通过 [GitHub Issues](https://github.com/Fingxing2025/sunyubao-project/issues) 联系；未获得书面许可前不得投入商业使用。
