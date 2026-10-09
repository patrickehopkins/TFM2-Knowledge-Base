# Camera, UI viewport and native action dispatch

Source: [Harbinger camera research](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/camera-research.md), [replay action analysis](https://github.com/patrickehopkins/TFM2-DirectControl/blob/main/docs/replay-native-action-analysis.md).

**Historical runtime-validated:** on the targeted 0.5.8/0.6.0 executables, the UI tree exposed battlefield viewport geometry, but did **not** expose spectator camera center and zoom. The logical render space reported as `1920 × 1080` while one observed physical client was `2560 × 1440`. Correct interaction requires explicit conversion between physical client pixels, logical UI coordinates and game-world space.

The historical native camera field map placed zoom/center/extents in offsets `+0xE0` through `+0xF0`; mode was `+0xF4` in 0.5.8 and shifted to `+0x100` in 0.6.0, while pan X/Y moved from `+0x418/+0x41C` to `+0x428/+0x42C`. This illustrates why **whole version-specific structures**, not only entrypoint RVAs, must be selected together.

**Versioned action handling:** Harbinger's 0.6.1 analysis traced a runtime action-to-binding getter used by live camera/input dispatch, allowing semantic replay actions to be blocked without assuming users retain default physical key bindings. The documented 0.6.2 profile used action IDs `0x1B` and `0x30..0x34`, but must not be copied into later builds without revalidation.

**Scope:** none of these details constitute a confirmed universal camera API or a demonstrated implementation on game 0.6.3. The original project code and exact-build guards control operational compatibility.
