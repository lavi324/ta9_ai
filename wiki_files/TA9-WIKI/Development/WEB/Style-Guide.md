**Mixins**

Use mixinis for the next css properties:

|css properties|mixin  |
|--|--|
|width and height |@dimensions($width, $height)|
|flex|@flex($justify-content, $align-items)|
|position|@position($position, $top, $right, $bottom, $left, $z-index)|
|vertical-center |@vertical-center($position)|
|ellipsis|@ellipsis|

Example:


```
.my-box {
        @flex(space-around, center);
	@position(absolute, null, 10px, 10px, null, 2);
}
```


will compiled to:


```
.my-box {
	display: flex;
	justify-content: space-around;
	align-items: center;
	position: absolute;
	right:  10px;
	bottom: 10px;
	z-index: 2;
}
```




**Colors** 
Always use colors variables from variables.scss
If the color does not exists define a new one.

```
$color1: #F8F8F8
$color2: #DAE2E6
     .
     .
     .
```

…

Example:


```
.my-box {
	background- color: $color13;
}
```






Import

To use mixins and colors you need to import main.scss:
`@import “main.scss”;`



