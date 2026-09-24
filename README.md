# Sunyu Baobao · Codex 桌宠素材库

这是「Sunyu Baobao」Codex 桌宠的版本化素材仓库，而不是一个独立运行的应用。每个版本包含可安装的宠物清单 `pet.json`、精灵图 `spritesheet.webp`，以及相应的验收记录、预览或制作资料。

> **许可与商用限制：**本仓库公开源代码和素材，但全部内容仅允许个人非商业使用。**未经书面授权，严禁任何形式的商业使用。**合作请通过 [GitHub Issues](https://github.com/Fingxing2025/sunyubao-project/issues) 联系，完整条款见 [LICENSE](LICENSE) 和 [ASSET_LICENSE.md](ASSET_LICENSE.md)。

## 最新版本

仓库新增 `codex-pet-idle-failed-swap` **待机与失落互换版**，基于 `codex-pet-foot-forward` 制作：

- 安装包：`孙煜宝宝-待机失落互换版.zip`
- 宠物 ID：`sunyu-baobao`
- 图集规范：Codex v1，`1536 × 1872`，`9 × 8` 格
- 更新范围：交换 `idle`（待机）与 `failed`（失落）的动作画面；其他 7 个动作保持不变

图集结构检查和未修改动作行检查记录见：

- `codex-pet-idle-failed-swap/final/validation.json`
- `codex-pet-idle-failed-swap/qa/row-preservation.json`
- `codex-pet-idle-failed-swap/qa/contact-sheet.png`

Codex v1 的待机槽固定为 6 帧、失落槽固定为 8 帧；本版本按原生槽位抽帧和延长帧数，不更改客户端节奏。安装后请在设置的宠物/Mini 列表中刷新并重新选择桌宠。素材校验不代表原生窗口已完成重载验收。

## 动作与触发条件

Codex v1 精灵图包含以下 9 种原生动作。动作由 Codex 客户端状态和桌面交互选择，精灵图只提供对应画面：

| 动作 | 触发条件 |
| --- | --- |
| `idle`（待机） | 没有更高优先级的任务状态或鼠标交互时，作为默认待机动作 |
| `running`（运行） | Codex 任务或工具处于 `Running` 活动状态 |
| `running-left`（向左移动） | 拖动桌宠约 4 px，且移动方向向左 |
| `running-right`（向右移动） | 拖动桌宠约 4 px，且移动方向向右 |
| `waving`（挥手） | 桌宠首次显示或从隐藏状态唤醒时 |
| `jumping`（跳跃） | 鼠标悬停在桌宠上 |
| `waiting`（等待） | Codex 状态为 `Needs input`，等待用户输入 |
| `review`（待查看） | Codex 状态为 `Ready`，任务已完成且有未读活动 |
| `failed`（失落） | Codex 状态为 `Blocked`，例如任务失败或系统错误 |

任务状态优先级为 `Needs input > Blocked > Ready > Running`。点击宠物随机播放动作目前不是原生触发方式；仅更换精灵图不能新增点击事件或随机切换逻辑。

## 安装待机与失落互换版

先解压 `codex-pet-idle-failed-swap/孙煜宝宝-待机失落互换版.zip`，其中会得到 `sunyu-baobao/` 文件夹。

1. 如已安装同名桌宠，先把现有 `sunyu-baobao` 文件夹改名或复制到安全位置备份。
2. 将解压出的 `sunyu-baobao/` 放到下列宠物目录：

   | 系统 | 目标目录 |
   | --- | --- |
   | macOS / Linux | `~/.codex/pets/sunyu-baobao/` |
   | Windows | `%USERPROFILE%\.codex\pets\sunyu-baobao\` |

3. 在 Codex 的设置中刷新宠物/Mini 列表，重新选择「孙煜宝宝」；如未加载，重启 Codex 后再次选择。

macOS / Linux 示例（这些命令会创建目标目录并覆盖同名的两个资源文件；执行前请完成第 1 步备份）：

```bash
unzip "codex-pet-idle-failed-swap/孙煜宝宝-待机失落互换版.zip" -d /tmp/sunyu-baobao-install
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
| `codex-pet-run-dynamics` | 动态跑步基线 | 大跨步、后脚腾空、反向摆臂；是 `codex-pet-foot-forward` 与互换版其余 7 个动作的来源 |
| `codex-pet-foot-forward` | 互换版的基础版本 | 两个方向动作改为赤脚脚底前伸，已生成最终安装包与验收材料 |
| `codex-pet-idle-failed-swap` | **最新版本** | 只调整 `idle` 与 `failed` 两个状态的画面；其他七个状态保持不变 |

较早目录主要用于回退、对照和复现；不要依据目录名称推断它们是当前默认安装版本。

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
- 发布新版本时，请把版本目录、安装包和 README 放在同一次提交中，避免仓库只有说明而缺少对应资源。
- 任何“已安装”或“可选中”的结论都应区分资源哈希、浏览器预览和 Codex 原生窗口三种验证层级。

## 许可、AI 与品牌声明

- Python、Shell、PowerShell、HTML、文档和配置等代码内容同样仅限个人非商业使用；本项目不采用允许商用的 MIT、Apache 或 GPL 等开源许可证。完整条款见 [LICENSE](LICENSE)。
- JPG、PNG、WebP、GIF、压缩包、嵌入 HTML 的人物图像，以及可识别的「Sunyu Baobao」角色形象，仅允许个人非商业使用；未经书面授权，严禁任何形式的商用、转售、再许可、广告代言、身份冒充、人脸识别或 AI 训练。完整条款见 [ASSET_LICENSE.md](ASSET_LICENSE.md)。
- 本项目的部分角色图像和动画由 AI 工具辅助生成或编辑，并经人工筛选、组装和校验。转载或发布相关素材时，应保留 AI 生成说明及依法、依平台规则需要保留的标识。
- 本项目是独立的非官方社区项目，与 OpenAI 不存在隶属、赞助或背书关系。OpenAI、Codex 及相关标识归其各自权利人所有。
- 合作、媒体使用或其他授权咨询，请通过 [GitHub Issues](https://github.com/Fingxing2025/sunyubao-project/issues) 联系；未获得书面许可前不得投入商业使用。
