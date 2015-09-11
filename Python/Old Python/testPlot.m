

str1 = 'testPointCloud.xyz';
str2 = 'testPointCloud2.xyz';
str4 = 'testPointCloudNELSON.xyz';
array = dlmread(str2, '\t');

x = array(:,1);
y = array(:,2);
z = array(:,3);

figure
%plot(x,y)
plot3(x,y,z)

axis equal
