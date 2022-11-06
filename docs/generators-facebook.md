# Facebook (`customblocks.generators.facebook`)

Embeds a [Facebook] post.

Page id and post id are the mandatory parameters for this component.

You can find them from the post url, obtained by clicking on the post date.
The url has the form:

`https://www.facebook.com/{pageid}/posts/{postid}`

::: warning
    Generated code will include user tracking from Facebook.
    User browser might, wisely, block the embed.

    A privacy safe version of this plugin is planned for the future.


[Facebook]: https://facebook.com


## Options

`page`
: Page (or user) id

`post`
: Post code.

You can obtain it from the url the post date points to.
Should be a public post in order to work.

`width` (keyword only, default 500)
: embed width (must be between 350 and 750)


## Example 

```markdown
::: facebook DesconexionIBEX35 pfbid0DXwq1fVjC7RRHjxqCevvrCuMaihZoSixKpJpUFxBQGGCPFEBGdkiKWYtZx4A6fGRl
```
::: facebook DesconexionIBEX35 pfbid0DXwq1fVjC7RRHjxqCevvrCuMaihZoSixKpJpUFxBQGGCPFEBGdkiKWYtZx4A6fGRl

```markdown
::: facebook lovokmon 10160236064339354 height=200
```

::: facebook lovokmon 10160236064339354 height=200


```markdown
::: facebook width=350 DesconexionIBEX35 pfbid0DXwq1fVjC7RRHjxqCevvrCuMaihZoSixKpJpUFxBQGGCPFEBGdkiKWYtZx4A6fGRl
```

::: facebook width=auto style="width:100%" DesconexionIBEX35 pfbid0DXwq1fVjC7RRHjxqCevvrCuMaihZoSixKpJpUFxBQGGCPFEBGdkiKWYtZx4A6fGRl

::: facebook notext width=350 DesconexionIBEX35 pfbid0DXwq1fVjC7RRHjxqCevvrCuMaihZoSixKpJpUFxBQGGCPFEBGdkiKWYtZx4A6fGRl



## TODO

- Obtain post information on static generation time and build a privacy safe place holder



