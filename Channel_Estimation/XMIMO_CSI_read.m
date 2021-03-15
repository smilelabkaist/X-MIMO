%
%=====================================================================================
%       Filename:  XMIMO_CSI_read.m
% 
%    Description:  load, differentiate, and convert the CSI data into imaginary and real signals.
%        Version:  1.0
%
%         Author:  Shuai Wang
%         Email :  <shine.hitcs@gmail.com>
%   Organization:  Smart and Mobile Systems (Smile) Lab @ KAIST 
%                  https://sites.google.com/view/smilelab/
%
%   Copyright (c)  Smart and Mobile Systems (Smile) Lab @ KAIST 
% =====================================================================================
%


% load the CSI, this requires the installation of Atheros CSI tool (matlab code).
csi=read_log_file('data_csi.txt');


antennas=zeros(length(csi),56*3);

antenna1=zeros(length(csi),56);
antenna2=zeros(length(csi),56);
antenna3=zeros(length(csi),56);


mix_antenna1=zeros(length(csi),56);
mix_antenna2=zeros(length(csi),56);
mix_antenna3=zeros(length(csi),56);

wifi_antenna1=zeros(length(csi),56);
wifi_antenna2=zeros(length(csi),56);
wifi_antenna3=zeros(length(csi),56);


% mixture_count is the number of CSI overlapped with ZigBee signal.
mixture_count=0;

% wifi_count is the number of CSI without ZigBee overlap.
wifi_count=0;
for i = 1:length(csi)
    csi_temp=csi{i,1}.csi;
 
    if csi_temp==0
       continue;
    end
    
    
    % record CSI on each antenna
    for j=1:56
        antenna1(i,j)=csi_temp(1,1,j);
        antenna2(i,j)=csi_temp(2,1,j);
       % antenna3(i,j)=csi_temp(3,1,j);
        antennas(i,j)=csi_temp(1,1,j);
        antennas(i,j+56)=csi_temp(2,1,j);
     %   antennas(i,j+56*2)=csi_temp(3,1,j);
    end
    
    % if payload size is 46, this is the second fragment, whcih overlaps
    % with ZigBee
	if csi{i,1}.payload_len==46
        mixture_count=mixture_count+1;
        for j=1:56
            mix_antenna1(mixture_count,j)=csi_temp(1,1,j);
            mix_antenna2(mixture_count,j)=csi_temp(2,1,j);
            % mix_antenna3(mixture_count,j)=csi_temp(3,1,j);
        
        end
    end  
    
     if csi{i,1}.payload_len==1896
        wifi_count=wifi_count+1;
         for j=1:56
         wifi_antenna1(wifi_count,j)=csi_temp(1,1,j);
        wifi_antenna2(wifi_count,j)=csi_temp(2,1,j);
       % wifi_antenna3(wifi_count,j)=csi_temp(3,1,j);
        
         end
    end       

end

% plot the amplitude of some the receveid CSIs:
figure();

hold on
for i=1:40
    plot(abs(antennas(i,:)));
end

% save CSIs into CSV files, from which the python code "zigbee_channel_calculation.py" would reconstruct
% overlappped ZigBee signal.

csvwrite('antenna1_wifi_csi_real.csv',real(ww_antenna1))

csvwrite('antenna1_wifi_csi_imag.csv',imag(ww_antenna1))

csvwrite('antenna1_mix_csi_real.csv',real(zz_antenna1))

csvwrite('antenna1_mix_csi_imag.csv',imag(zz_antenna1))

csvwrite('antenna2_wifi_csi_real.csv',real(ww_antenna2))

csvwrite('antenna2_wifi_csi_imag.csv',imag(ww_antenna2))


csvwrite('antenna2_mix_csi_real.csv',real(zz_antenna2))

csvwrite('antenna2_mix_csi_imag.csv',imag(zz_antenna2))




