# X-MIMO
Welcome to our Corss-technology Channel Estimation Tool. Out tool consists of two parts: (i), fragments injection, which injects the customized WiFi fragments with precise timing control. (ii), channel estimation, which estimates the cross-technology channel from the channel state information (CSI) collected from the injected fragments. Our implementation follows the design in [[1]](#1) and supports collecting the cross-technology channel information at a wireless router (TP-link WDR4300) or an Atheros WNIC as long as they support Atheros CSI Tool [[2]](#2). 

To understand how our tool is operated, we provide two demos for wireless router users:

[![Watch the video](http://mason.gmu.edu/~swang42/resources/text3082-4-6-1-6-6-1-1.png)](https://youtu.be/zoNW761Damo)

And WNIC users:

[![Watch the video](http://mason.gmu.edu/~swang42/resources/system_2.png)](https://youtu.be/zoNW761Damo)

You can find the detailed instruction in [this PDF file](https://github.com/smilelabkaist/X-MIMO/blob/master/Cross_technology_Channel_Estimation_Tool_User_Guide.pdf). If you apply our tool in your research, please cite our paper [[1]](#1). For tourbleshooting, please contact Shuai: shine.hitcs@gmail.com. 

## Reference
<a id="1">[1]</a> 
Shuai Wang, Woojae Jeong, Jinhwan Jung, and Song Min Kim. "X-MIMO: cross-technology multi-user MIMO." In Proceedings of the 18th Conference on Embedded Networked Sensor Systems, pp. 218-231. 2020.

<a id="1">[2]</a> 
Yaxiong Xie, Zhenjiang Li, and Mo Li. "Precise power delay profiling with commodity Wi-Fi." IEEE Transactions on Mobile Computing 18, no. 6 (2018): 1342-1355.
