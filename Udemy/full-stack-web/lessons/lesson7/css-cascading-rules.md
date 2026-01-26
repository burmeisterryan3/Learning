# CSS - Cascading Rules

CSS applies styling in a series of cascading rule sets. These rules are defined here for reference.

## Position

> CSS rules cascade such that, if the same styling rule is defined multiple times, the last rule will be applied.

In the below example, because `color:blue` is defined after `color:red`, it is applied.

```
<ul>
  <li>One</li>
  <li>Two</li>
  <li>Three</li>
</ul>
```

```
li {
    color: red;
    color: blue;
}
```

## Specificity

> CSS rules cascade such that the more specific rule is the one applied.

1. Element (Least specific)
2. Class
3. Attribute
4. Id (Most specific)

In the below example, `#first-id {color:orange;}` is applied as it is the most specific rule.

```
<li id="first=id" class="first-class draggable>Example</li>
```

```
li {color: blue;}
.first-class {color: red;}
li[draggable] {color:purple;}
#first-id {color:orange;}
```

## Type

> CSS rules cascade such that the most specific location is the one applied.

1. External
2. Internal
3. Inline

In the below example, the style applied inline (`<h1 style=" ">Hello</h1>`) is the most specific location and is the one shown.

```
<link rel="stylesheet" href="./style.css">
<style></style>
<h1 style=" ">Hello</h1>
```

## Importance

> CSS rules cascade such that an _important_ rule is the one applied.

This rule is applied when the `!important` annotation is applied to a style.

```
color: red
color: green !important;
```

## Cascading Categories

> CSS rules are applied such that the higher precedence rule is applied.

Given the multiple cascading levels for CSS rules, it is important to note that these categories are themselves applied in a particular order. Thus, if the same style were defined in multiple locations, the highest precdent rule would be the one applied.

1. Position (lowest precedence)
2. Specificity
3. Type
4. Importance (highest precedence)
