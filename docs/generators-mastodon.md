# Mastodon (`customblocks.generators.mastodon`)

Embeds a Mastodon post.
[Mastodon](https://joinmastodon.org) is the federated social network for short posts.

Federated means that users might choose the server to have the account on,
just like email, and the servers talk with each other to provide the service.
Because of that you should provide `server`, `user` and `post`.

Post urls have this form: `https://{server}/{user}/{post}`
for example: `https://mastodon.social/@trwnh/99664077509711321`.

If you are browsing a list of posts or a thread,
you can obtain the url to the specific post by clicking on the date.

## Example

```markdown
::: mastodon mastodon.social @trwnh 99664077509711321
```

::: mastodon mastodon.social @trwnh 99664077509711321

```markdown
::: mastodon mastodon.social @votomitico 101638382345543997
```

::: mastodon mastodon.social @votomitico 101638382345543997

## Options

`server`
: mastodon instance where the user lives

`user`
: the user that wrote the publication

`post`
: the publication id (a long number)


## TODO

- Accept users as `@user@server`
- Accept post url


