# CHANGELOG

<!-- version list -->

## v0.1.16 (2026-10-19)

### Bug Fixes

- Handle optional VK API fields via .get() in api_based, events, user
  ([`257ef45`](https://github.com/djachenko/pyvko/commit/257ef4527cb37f06dc89a50cd242c1ff17c39304))

- Pass positive group_id in Group.get_members
  ([`39c7765`](https://github.com/djachenko/pyvko/commit/39c77655057e097179e4e4d1b34c88ea3e9f068c))

### Chores

- Ignore .env and CLAUDE.local.md, remove BACKLOG.md, add pytest-dotenv
  ([`c9419b5`](https://github.com/djachenko/pyvko/commit/c9419b52bc25b203b6379a4b3ad07be41c5c1223))

- Ignore _worktrees and memory dirs
  ([`c1cd357`](https://github.com/djachenko/pyvko/commit/c1cd357407e1c60e3204fab9856042f44dc50109))

- Register pytest markers smoke and create
  ([`ebb207f`](https://github.com/djachenko/pyvko/commit/ebb207f168899bb9e82607beb03a6bc71efa05fc))

### Code Style

- Make id-sign method tables private with multiline dicts
  ([`a7e6a9a`](https://github.com/djachenko/pyvko/commit/a7e6a9a67cb35590c519c8e13fc519b9fdc3fc5c))

- Separate test phases with blank lines
  ([`4b620ec`](https://github.com/djachenko/pyvko/commit/4b620ec3a797e6a0dfd993383208047c19e5b527))

### Documentation

- Drop status, backlog and Python version from CLAUDE.md
  ([`0bce4b9`](https://github.com/djachenko/pyvko/commit/0bce4b988a7011257fc12aa7836df1f5979e693c))

- Update CLAUDE.md — version, status, backlog
  ([`6b04177`](https://github.com/djachenko/pyvko/commit/6b041770cfb3b3c57f4fbb289aab7d962e042bb8))

### Refactoring

- Clean up get_token — remove hardcoded Windows paths, all scopes, https redirect
  ([`fab0ef8`](https://github.com/djachenko/pyvko/commit/fab0ef868cbc1afcad19e10975b9acc168dd7abc))

- Replace None pre-init with explicit if/else in Event
  ([`ac5a1ec`](https://github.com/djachenko/pyvko/commit/ac5a1ec9f566ac13dba130a64ff0cec9635f4de4))

### Testing

- Add integration tests
  ([`2f15f88`](https://github.com/djachenko/pyvko/commit/2f15f88a9437bd529e6c04d6caf1178b6ec41470))

- Add read-only tests for existing event via VK_TEST_EVENT_ID
  ([`107fb20`](https://github.com/djachenko/pyvko/commit/107fb20f4e63f81875b698336d219985c8773791))

- Add VK API surface detector for silently removed methods
  ([`04431e2`](https://github.com/djachenko/pyvko/commit/04431e2223ad8ab9f333354d01b297510d67e5c6))

- Add wall photo upload and post with attachment tests
  ([`5181d43`](https://github.com/djachenko/pyvko/commit/5181d43169b82ca9eed354a81862540fd36fda77))

- Add wall_photo and test_event fixtures to conftest
  ([`82f775a`](https://github.com/djachenko/pyvko/commit/82f775a6afd5f48cfd029d4c08e2066f53201584))

- Group mixed-fixture tests into classes
  ([`8be8304`](https://github.com/djachenko/pyvko/commit/8be830471ceeeea8ee1b59f901285497d05f8d1b))

- Pin group_id/owner_id sign convention against live VK API
  ([`faf638a`](https://github.com/djachenko/pyvko/commit/faf638a380ac1bf298a31340b051f332d89912ed))

- Pin group_id/owner_id sign per VK method
  ([`2e41f85`](https://github.com/djachenko/pyvko/commit/2e41f85c5d3adb9f66adf7abf1ab3f2824ca1e7b))

- Rename created_event tests shadowed by read-only event tests
  ([`35d8f6f`](https://github.com/djachenko/pyvko/commit/35d8f6f34d9b30edf481377a73a4cad532fd5195))


## v0.1.15 (2026-10-06)

### Bug Fixes

- Quote Group annotation so pyvko imports on Python 3.10–3.13
  ([`9e1cbeb`](https://github.com/djachenko/pyvko/commit/9e1cbeb8bb7ec9cf1997f654906be094dc5320cc))

### Chores

- [repokit] add Claude skill for repokit integration
  ([`ed5818a`](https://github.com/djachenko/pyvko/commit/ed5818a6a40401ba4625fdd2e3064a6b21b75dfe))

- [repokit] update ci workflows
  ([`8f3a72e`](https://github.com/djachenko/pyvko/commit/8f3a72e0355e3338cd827263c6ed401bcee113c2))

### Refactoring

- Replace quoted annotations with postponed evaluation
  ([`9b071b9`](https://github.com/djachenko/pyvko/commit/9b071b9b718b5be04c54011e5a348d681df69262))

### Testing

- Drop local python matrix covered by repokit integration
  ([`d6af101`](https://github.com/djachenko/pyvko/commit/d6af1017594bb8b36567687b8416d8529198b607))

- Import every module on Python 3.10–3.14
  ([`bf9f82b`](https://github.com/djachenko/pyvko/commit/bf9f82b0489c0e948059e74457e50dd7e0536852))


## v0.1.14 (2026-10-04)

### Bug Fixes

- Declare runtime dependencies in pyproject.toml
  ([`961de41`](https://github.com/djachenko/pyvko/commit/961de418b26a5df8c25a9767c18492e267c7d231))

### Build System

- Pin ruff below 0.16 in test extras
  ([`f09b0c2`](https://github.com/djachenko/pyvko/commit/f09b0c2203c450a77cdf321b56f685564583a51c))

### Chores

- Remove setup.py and requirements.txt duplicating pyproject.toml
  ([`51ec2b5`](https://github.com/djachenko/pyvko/commit/51ec2b5b7004a01885958771a8debae64c71c88a))


## v0.1.13 (2026-07-05)

### Bug Fixes

- Resolve circular import between Group and User
  ([`e1d923b`](https://github.com/djachenko/pyvko/commit/e1d923bbe33bdabd2abe912b1c16497224da48e2))


## v0.1.12 (2026-06-24)

### Bug Fixes

- Dict = None → Dict | None across api_based, albums, reposts
  ([`1ca5214`](https://github.com/djachenko/pyvko/commit/1ca52143341b97f6c974c8cc0e7c550b11335e82))

- Fixed repokit dependencies
  ([`a57c1a3`](https://github.com/djachenko/pyvko/commit/a57c1a35be16b6b707edccf316de0c108fd63648))

- Fixed ruff errors
  ([`c7d9170`](https://github.com/djachenko/pyvko/commit/c7d91703b0d0afab095177cbc1acb85c05a64c2a))

- Get_all and PhotoUploader type signatures
  ([`71912f8`](https://github.com/djachenko/pyvko/commit/71912f8cb77ef7af7c9d2049bc23fa0c402b14d6))

- Groups imports — remove tokenize shim, add Any/TYPE_CHECKING
  ([`b9f4da0`](https://github.com/djachenko/pyvko/commit/b9f4da045e4c026794a467d9099b665cb7cfa7f1))

- Link stub properties raise NotImplementedError, photo_object typed as Any
  ([`d9f8445`](https://github.com/djachenko/pyvko/commit/d9f844519116f53a05b083263326400707d1e1ad))

- Migrate pyvko_main and events self.api → self.new_api
  ([`d0da0ca`](https://github.com/djachenko/pyvko/commit/d0da0ca6adbe86e16c7ff8373425e51896d4f1cf))

- Nullable fields in PostModel, Post, CommentModel
  ([`2409ec1`](https://github.com/djachenko/pyvko/commit/2409ec19f66b83b1fd1de3b55b64428df76cec28))

- Precise mypy override for vk_api, remove types-requests from deps
  ([`47d47b3`](https://github.com/djachenko/pyvko/commit/47d47b39be635154fb52c4f4c42fa5aba66dac2e))

- Remove API=Any shims, replace api: API type hints with Any
  ([`c5f8054`](https://github.com/djachenko/pyvko/commit/c5f8054d57e57ad003f5cd40d7f7af96653d59b7))

### Chores

- [repokit] add pyproject.toml
  ([`ce1ad58`](https://github.com/djachenko/pyvko/commit/ce1ad582c160191b966bbf5aeab28f270c2a47fc))

- [repokit] save language config
  ([`c795b9e`](https://github.com/djachenko/pyvko/commit/c795b9e2b92bd6f0df68632029d1330166b3abc8))

- [repokit] update ci workflows
  ([`86a4a5e`](https://github.com/djachenko/pyvko/commit/86a4a5e2500a02494cf84d2b51bd04c8ee861d08))

- [repokit] update ci workflows
  ([`3a57a9f`](https://github.com/djachenko/pyvko/commit/3a57a9f8cce872d30f8ae0844d8f82bb59382453))

- [repokit] update ci workflows
  ([`0aa7ff9`](https://github.com/djachenko/pyvko/commit/0aa7ff99222c69f98d61adefdaabf1ab91b88f77))

- Add pyproject.toml for modern build config
  ([`95807db`](https://github.com/djachenko/pyvko/commit/95807db5f2a1bec5647350004d7566dca28001f8))

- Exclude pyvko_runner from mypy, add BACKLOG
  ([`4b83662`](https://github.com/djachenko/pyvko/commit/4b836622854d7617b1b68ef5b69498c1ad014483))

- Ignore missing stubs globally, document in BACKLOG
  ([`c9c21f8`](https://github.com/djachenko/pyvko/commit/c9c21f89226346906d72b78f1c4a5072ab85693f))

- Replace vk with vk_api dependency
  ([`799c733`](https://github.com/djachenko/pyvko/commit/799c733c3203b30ca86a4c92ddf1dded92306d88))

- Replace vk.API type hints with Any
  ([`6067fd9`](https://github.com/djachenko/pyvko/commit/6067fd97bb6686b64a45aaf8aec7d78aafcbd1b9))

- Restore version to 0.1.11 for PSR
  ([`8a91233`](https://github.com/djachenko/pyvko/commit/8a91233b1e3dd93560281f83f85e54a610256ff8))

### Documentation

- Add CLAUDE.md project guide
  ([`ab1eaf7`](https://github.com/djachenko/pyvko/commit/ab1eaf7d30cac619fb4d722ec663de2d9857b4ce))

### Refactoring

- Add api fail-fast property to ApiMixin and ApiBased
  ([`19374ca`](https://github.com/djachenko/pyvko/commit/19374cac033132744652691f2f561989e7b6c35b))

- Migrate remaining api→new_api calls, fix groups imports
  ([`e4d07cb`](https://github.com/djachenko/pyvko/commit/e4d07cb6aed966208a8626b6d10ecd295f21d039))

- Migrate to src layout
  ([`dcb16e4`](https://github.com/djachenko/pyvko/commit/dcb16e415ccd1160addd14296d26f2a9c0557048))

- Remove CaptchedApi, add native vk_api captcha handler
  ([`76eba5a`](https://github.com/djachenko/pyvko/commit/76eba5ac10531acd20dbc932d7ce4f3e30c133a9))

- Rename api→new_api, migrate active upload code paths to vk_api
  ([`9b33460`](https://github.com/djachenko/pyvko/commit/9b334600f1e5a988f87cb349ecb4a6c1b483c1bd))


## v0.0.1 (2026-06-24)

- Initial Release
