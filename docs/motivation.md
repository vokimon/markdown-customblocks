# Motivation

This text explains the motivation to write this extension
and the rationale under the design decissions.

Many custom objects like figures, video embeds...
have no native markup in Markdown.
No problem: you can still hardcode them in HTML
or you could also use an extension for that.

Hardcoding HTML has a clear drawback:
Besides cluttering the markdown with HTML,
whenever we need to upgrade the block,
(eg. adding a lightbox feature for all the figures)
you have to change that code in many places.

Extensions have other problems,
mostly because of the dynamics of creating and maintaning them.

First, 
extensions struggle to use a unique markup to avoid conflicts with other extensions.
Because of that, the trend is having a lot of different markups,
even for extensions sharing the same purpose.

And second, why is that so many extension sharing
the same purpose (and using so different markups).
Maybe is because the feature set of the original
extension is kept and someone comes with a

First, because you don't want to mess existing extension users,
whenever a new breaking feature appears
First, in order to identify their own markup,
extensions have to define a diferential markup.
Even if extensions have the same semantics they tend to have differentiable markups.





until you want to improve them, say changing the `div` structure.
Then, you have to make the change extensive to
all the objects in your documentation, and that's hard.

Luckily, many Markdown extensions are available
which encapsulate such objects in custom fancy markups.
But the way such extensions are created and maintained have two major drawbacks:

When you find a better extension for your figures,
again, it is likely you have to edit all your figures, once more,
because the markup is different.

Also coding an extension is hard.
Markdown extension API is necessarily complex to address many scenarios.
But this extension responds just to this single but general scenario:

> I want to generate this **piece of HTML** which
> depends on those **parameters** and might
> include a given **content**.

So...

**Why using a common markup for that many different structures?**

This way, markup syntax explosion is avoided,
and users do not have to learn a new syntax.
Also, developing new block types is easier if you can reuse the same parser.

**Why using a type name to identify the structure?**

A name, as part of the markup, clarifies the block meaning on reading.
Also provides a hook to change the behaviour while keeping the semantics.
If you do not like the predefined generator for a given type,
you can provide a new generator with your extended features.

**Why defining a common attribute markup?**

A common attribute markup is useful to stablish a general mapping
between markup attributes and Python function parameters.
The signature of the generator function defines the attributes that can be used
and the extension does the mapping with no extra glue required.

**Why using indentation to indicate inner content?**

It visually shows the scope of the block and allows nesting.
If the content is reparsed as Markdown,
it could still include other components with their inner content a level deeper.


