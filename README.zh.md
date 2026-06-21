<div align="center">

# Any2Clawd

*"用自然语言，让 Claude Code 动起来。"*

<img src="assets/cover.png" alt="Any2Clawd" width="600">

![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB)
![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-8A2BE2)

🦀 一个由自然语言驱动的 **Clawd** 像素小螃蟹 SVG 动画生成器，以 Claude Code skill 的形式封装。

🔧 只要说一句"clawd 喝咖啡"或"小螃蟹困惑挠头"，skill 就会把它做成一个可循环播放的像素动画，并导出成能直接发进聊天软件的 GIF 表情。

[安装](#安装) · [使用](#制作一个表情) · [画廊](#画廊) · [导出 GIF](#导出-gif) · [English](README.md)

</div>

---

🌟 本项目由此前本人在微信表情包平台发布的两套表情《螃蟹 CC 的日常》的开发流程整理而成。形象取自 Claude Code 的吉祥物 Clawd，在 [clawd-tank](https://github.com/marciogranzotto/clawd-tank) 项目公开的 Clawd 素材基础上延伸创作。

🔥 上线的两个月里这两套表情包收获了 **6w+ 次下载和 130w+ 次发送**，非常感谢大家的支持 ☺️！不过因为微信平台不允许同人创作类表情，这两套表情都已经遗憾下架 😢——已下载的用户不影响使用，还未下载的朋友仍然可以通过直接保存源文件来获取表情～

🖼️ 在[画廊](#画廊)里展示了部分已发布的表情和一些新的表情，完整的 GIF 表情文件都在 `wechat_stickers/` 文件夹中。
## 安装

需要 **Python 3.10+** 和系统里的 **Chrome/Chromium**（用来渲染动画帧；若装在非默认位置，用 `CHROME` 指定路径）。

```bash
git clone https://github.com/Yuriceee/Any2Clawd.git
cd Any2Clawd
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 关于 skill

skill 放在 `.claude/skills/any2clawd/`，在仓库根目录运行 `claude` 时会自动加载，不用额外安装。

它是一个**项目级SKILL**：规则文档读自 `docs/`，参考素材取自 `assets/` 素材库，渲染和导出则交给 `tools/`——这些都在本仓库里。所以请保持仓库完整，并在根目录运行生成。（只把 `any2clawd/` 文件夹单独安装可能会有问题，因为那样会丢掉 `docs/`、`assets/` 和 `tools/`的参考文件。）

## 制作一个表情

在仓库根目录启动 Claude Code，SKILL会自动加载：

```bash
claude
```

然后用自然语言描述你想要的效果：

```text
clawd 喝咖啡的动画
帮我做一个小螃蟹困惑挠头的表情
画个像素小螃蟹踢足球
```

新生成的 SVG 会出现在 `workspace/`（一个本地草稿区）。你可以**反复多轮地打磨**："帽子往左挪一点""节奏再快些""球衣换成红色"——agent 会跟着改。改到满意了，直接跟它说"**帮我把这个表情存档**"，它就会替你跑存档步骤；当然你也可以自己来：

```bash
python tools/promote_svg.py --promote clawd-<name>
```

第一次存档时，它会让你给自己的合集起个名字（比如用你的用户名），之后你的表情就会收进 `assets/<name>/`。

## 画廊

`assets/` 既是项目的动画**画廊**，也是 skill 的少样本（few-shot）知识库——每个动画都配了一段结构化的描述文字，skill 生成新动画时会拿它们当参考。下面是其中一部分：

| | | | | | |
|:-:|:-:|:-:|:-:|:-:|:-:|
| ![](wechat_stickers/clawd-kick-messi.gif) | ![](wechat_stickers/clawd-flying-kiss.gif) | ![](wechat_stickers/clawd-sick.gif) | ![](wechat_stickers/clawd-surrender-helpless.gif) | ![](wechat_stickers/clawd-ok-nodding.gif) | ![](wechat_stickers/clawd-innocent-blink.gif) |
| 踢球 | 飞吻 | 生病 | 没招了 | ok | 可爱 |
| ![](wechat_stickers/clawd-congrats-tophat.gif) | ![](wechat_stickers/clawd-crying.gif) | ![](wechat_stickers/clawd-approved.gif) | ![](wechat_stickers/clawd-running.gif) | ![](wechat_stickers/clawd-drowsy.gif) | ![](wechat_stickers/clawd-snake-charmer.gif) |
| 恭喜 | 哭泣 | 对的 | 奔跑 | 燃尽了 | python（舞蛇） |

画廊按命名合集来组织：

- `assets/upstream/` — 沿用 clawd-tank 的基础动画（只读）
- `assets/original/` — 项目自有的动画库（只读）
- `assets/<你的名字>/` — 你自己的合集（`promote_svg.py` 会问你要名字）

里面带描述的优质动画越多，skill 就做得越好。😎 **做出了满意的表情？欢迎贡献**——提个 PR，把你的动画（`svg` + `caption`）加到某个合集下，再把对应 GIF 放进 `wechat_stickers/`，一起拓展这个公共知识库。

## 导出 GIF

直接让 agent "导出 GIF"，或者自己跑导出工具：

```bash
python tools/svg_to_gif.py \
  --input workspace/clawd-<name>.svg \
  --output workspace/gif/clawd-<name>.gif
```

导出工具会**自动裁到动画范围，再缩放成规整的 240×240 方形**，让 Clawd 始终保持合适的大小，省去手动裁剪。最后得到的是一张透明、可循环的 **GIF 表情**（体积很小，通常远不到 500 KB），可以直接发进微信或任意聊天软件。（本人在开发微信表情的过程中经过了漫长的调试...当前版本应该能较好的适配微信系统）

有些客户端对透明 GIF 的支持不太好，碰到这种情况加上 `--background white` 即可。

## 致谢与许可

代码采用 MIT 许可证。Clawd 的基础角色设计参考了开源项目
[clawd-tank](https://github.com/marciogranzotto/clawd-tank)（MIT）；素材的使用政策
详见 [ASSETS.md](ASSETS.md)。"渲染后再看一眼"的检查思路，则受
[clawd-emotes-skill](https://github.com/xixicc186/clawd-emotes-skill) 启发。
