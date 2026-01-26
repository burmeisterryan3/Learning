# CSS Positioning

This page discusses the various positioning schemes using HTML and CSS.

There is also a [demo site](https://appbrewery.github.io/css-positioning/) that allows for viewing these in a simple format.

## Overview

CSS positioning allows for the placement of web elements on a site.

The `position` property specifies the scheme of positioning while the `top`, `right`, `bottom`, and `left` properties allow for more fine grained control wihtin the selected scheme.

The positioning schemes include `static`, `relative`, `fixed`, `absolute`, and `sticky`.

## Static

Any element with the static scheme follows the normal flow of the page. The properties `top`, `right`, `bottom`, and `left` have no effect.

Statis is the default behavior. Thus, if the position attribute is not defined, then it will have the static position scheme.

```
position: static;
left: 50px;
top: 50px;
```

## Relative

Any element with the relative scheme is positioned relative to the normal document flow. Setting the `top`, `right`, `bottom`, and `left` properties adjust the element relative to its normal position.

```
position: relative;
left: 50px;
top: 50px;
```

## Fixed

Any element with the fixed position is positioned relative the browser, or viewport. Even when scrolled, the element does no move. The `top`, `right`, `bottom`, and `left` properties adjust the position relative the top left of the view port.

```
position: fixed;
top: 50px;
left: 50px;
```

## Absolute

Any element with the absolute position is positioned relative to its closest ancestor that is also positioned. (NOTE: This does not include static)

Elements using absolute positioning can overlap other elements.

```
position: absolute;
top: 50px;
left: 50px;
```

## Sticky

Any element with the sticky position is positioned in a fashion between relative and fixed. The position of the element is relative until a particular scroll position is reached, at which point, it is fixed at that position.

Example: A box that starts in the middle of a page gets stuck at the top once you scroll down.

```
position: sticky;
top: 50px;
left: 50px;
```
