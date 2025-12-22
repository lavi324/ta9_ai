## **How to use svg** 

In order to display svg you need to use svg-icon component

![image.png](/.attachments/image-8b59d569-3434-4993-a472-f5ccc39a7b1e.png)

you can find the svg-component api here: 
https://www.npmjs.com/package/angular-svg-icon



## **svg style**

you can style the svg with css. for example: 

![image.png](/.attachments/image-7cacb2df-874f-4e30-81fe-93f02c495aff.png)



## **See all available icons**
To see and search ta9 icons navigate to http://10.100.102.24/ng/ta9-icons
![image.png](/.attachments/image-c065d404-bf76-4aca-993e-8952a36ef2e3.png)



## **Adding new icon**
All the icons are placed in assets/svg/icons.
When you adding new icon you need do 2 things:

1. verify that there is no generic classes in the svg (e.g class="a").
if there is a generic class you need to change it by adding the icon name as suffix. 
for example to icon star.svg:  class="a" need to be changed to class="a-star"
![image.png](/.attachments/image-3f3573a9-c2eb-45c2-85e3-179081cf6c5f.png)

2. add the icon path to Ta9IconsComponent (to svgIcons array)
![image.png](/.attachments/image-e9fc5196-845e-4953-8ff7-1e4082e61b2a.png)




