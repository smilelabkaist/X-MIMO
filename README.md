# Cross-technology Channel Estimation Tool
Welcome to our Cross-technology Channel Estimation Tool. Our tool consists of two parts: (i), fragments injection, which injects the customized WiFi fragments with precise timing control. (ii), channel estimation, which estimates the cross-technology channel from the channel state information (CSI) collected from the injected fragments. Our implementation follows the design in [[1]](#1) and supports collecting the cross-technology channel information at a wireless router (TP-link WDR4300) or an Atheros WNIC as long as they support [Atheros CSI Tool](https://wands.sg/research/wifi/AtherosCSI/). 

To understand how our tool is operated, we provide two demos for [wireless router users](https://youtu.be/zoNW761Damo) and [WNIC users](https://youtu.be/HPsjK79-gDY). The detailed instruction can be found in [this PDF file](https://github.com/smilelabkaist/X-MIMO/blob/master/Cross_technology_Channel_Estimation_Tool_User_Guide.pdf). 

If you apply our tool in your research, please cite our paper [[1]](#1). For troubleshooting, please contact Shuai: shine.hitcs@gmail.com. 

## Reference
<a id="1">[1]</a> 
Shuai Wang, Woojae Jeong, Jinhwan Jung, and Song Min Kim. "X-MIMO: cross-technology multi-user MIMO." In Proceedings of the 18th Conference on Embedded Networked Sensor Systems, pp. 218-231. 2020.

