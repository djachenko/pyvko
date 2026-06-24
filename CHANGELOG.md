# CHANGELOG

<!-- version list -->

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
