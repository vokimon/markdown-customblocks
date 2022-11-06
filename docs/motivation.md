# Motivation

This text explains the motivation to write this extension
and the rationale under the design decissions.

Many custom objects like figures, video embeds...
have no native markup in Markdown.
You could hardcode them as HTML
or you could also use an extension for that.

Hardcoding HTML has a clear drawback:
Besides cluttering the markdown with HTML,
whenever we need to upgrade the block,
because you found a better way of embeding videos or whatever,
you have to change that code in many places.

Extensions avoid the HTML clutter,
but, still they are not useful to upgrade your blocks.
Usually improving a block means moving to a different extension,
with more features.
But extensions, in order to avoid collisions, 
tend to be creative on the markup they use,
even if they cover the same function.
So if you migrate to a more powerfull extension,
you end up editing all your blocks again.

Another motivation is that coding an extension is hard.
Markdown extension API is necessarily complex to address many scenarios.
But this extension responds just to this single but quite general scenario:

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

**Why functions as means for extension?**

Well, it is simpler than having class interfaces,
and Python introspection helps a lot to do the parameter mapping.


