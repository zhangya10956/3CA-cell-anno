%% 这里是我自己刚才测试HOG特征的一段代码，没什么用
% %% 测试HOG特征
% clear all; close all; clc;
% img=imread('yangLi1.png');
% im=imresize(img,[64,64]);  
% % 由于是灰度图像，就不需要由RGB转成灰度了
% % img=rgb2gray(im);  
% % 这里用的是MATLAB自带的HOG特征提取器，我也不知道什么是HOG特征，但是看网上对图像做SVM分类时都是用的这个，可以上网看看
% [featureVector,hogVisualization] = extractHOGFeatures(im); 
% data(1,:)=featureVector;  
% imshow(im);
% hold on;
% plot(hogVisualization);




%% 用hog特征对图像进行多分类，svm训练，1 VS 1    
%% 1 数据集，包括训练的和测试的 (注意自己图片存放路径) 
% clear;
% imds = imageDatastore('F:\Dataset\ICPR_HEp2016',...    
%     'IncludeSubfolders',true,...    
%     'LabelSource','foldernames'); 
% 
% imds = shuffle(imds);% 打乱数据顺序
% [imdsTrain,imdsTest] = splitEachLabel(imds,0.8,0.2);% 划分数据集
imdsTrain = imageDatastore('D:\PyCharm Community Edition 2021.2.3\dataset\DBSY\scMRA\10X-Smart\Trachea\0415-concat-1-HVG2000\train',...             %直接更改路径就行了
    'IncludeSubfolders',true,...    
    'LabelSource','foldernames');   
imdsTrain = shuffle(imdsTrain);% 打乱数据顺序


% 不知道你有没有测试集，如果有测试集，则需要下面的这行代码
% 如果没有测试集，可以使用训练集看一下在训练集上的效果。
% 但是如果可以的话，可以将上面的训练集拆分，splitEachLabel函数可能有用，但是我也没用过，可以参考一下

imdsTest = imageDatastore('D:\PyCharm Community Edition 2021.2.3\dataset\DBSY\scMRA\10X-Smart\Trachea\0415-concat-1-HVG2000\test',...                %直接更改路径就行了
    'IncludeSubfolders',true,...    
    'LabelSource','foldernames');    
  
  
%% 显示训练的图片种类Labels和数量Count  
numTrain = length(imdsTrain.Files); 
Train_disp = countEachLabel(imdsTrain);  
TrainLabels = imdsTrain.Labels;
disp(Train_disp);  
    


%% 预测并显示预测效果图 
% 如果有测试集，则运行这一段；
numTest = length(imdsTest.Files);  
% featureTest1 = zeros(numTest,size(lbpFeaturestrain,2),'single');
% featureTest2 = zeros(numTest,size(hogfeaturestrain,2),'single');
% featureTest = zeros(numTest,size(features,2),'single');
% testimage1 = readimage(imdsTest,1);    
% scaleImagetesttest = imresize(testimage1,imageSize); 
% 所有测试图像标签 
Test_disp = countEachLabel(imdsTest);
TestLabels = imdsTest.Labels; 

% acc = 0;
% acc1 = 0;
% acc2 = 0;
% acc3 = 0;
% acc4 = 0;
% acc5 = 0;
% acc6 = 0;
%featuresTest1是LBP特征
% lbpFeaturestest = extractLBPFeatures(scaleImagetesttest,'CellSize',[lbp_CellSize lbp_CellSize],'Normalization',Normalization,'Upright',Upright);
% featuresTest1 = zeros(numTest,size(lbpFeaturestest,2),'single'); % featuresTest1为双精度，不然会报错
%featuresTest2是HOG特征
% [hogfeaturestest,visualization] = extractHOGFeatures(scaleImagetesttest);
% 'CellSize',[hog_CellSize hog_CellSize],'BlockSize',[hog_BlockSize hog_BlockSize],'NumBins',NumBins);
% featuresTest2 = zeros(numTest,size(hogfeaturestest,2),'single'); % featuresTest1为双精度，不然会报错






% train_PCA
% featuresTrain = zscore(imdsTrain);
featuresTrain = zeros(numTrain:2000);
% % 稀疏矩阵
% featuresTrain = sparse(numTrain:2000);
for ii=1:numTrain
    trainImage = readimage(imdsTrain,ii);
    trainImage = reshape(trainImage,1,2000);
%     scaleTestImage = imresize(testImage,imageSize)
    
    featuresTrain(ii,:) = trainImage;
end
featuresTrain = zscore(featuresTrain);




% test_PCA
% featureTest = zscore(imdsTest);
% % 总的featuresTest，内存不够
featuresTest = zeros(5705:2000);        %原来是zeros(numTest;:2000);     numTest时显示内存不够，就是不运行
% 稀疏矩阵
% featuresTest = sparse(numTest:2000);
for iii=1:numTest
    testImage = readimage(imdsTest,iii);
    testImage = reshape(testImage,1,2000);    
    featuresTest(iii,:) = testImage;
end

featuresTest = zscore(featuresTest);





% % 分的featuresTest
% numTest1 = numTest/2;
% featuresTest1 = zeros(numTest1:2000);
% for iii=1:numTest1
%     testImage = readimage(imdsTest,iii);
%     testImage = reshape(testImage,1,2000);    
%     featuresTest1(iii,:) = testImage;
% end
% 
% 
% numTest2 = numTest - numTest1;
% featuresTest2 = zeros(numTest2:2000);
% for iiii = (numTest2+1):numTest
%     testImage = readimage(imdsTest,iiii);
%     testImage = reshape(testImage,1,2000);    
%     featuresTest2((iiii-numTest2),:) = testImage;
% end
% 
% featuresTest = [featuresTest1;featuresTest2];
% % % 分的featuresTest





featuresTrainTest = [featuresTrain;featuresTest];

[coeff,latent,explained]=pcacov(featuresTrainTest);

%1设定方差贡献度为99%
for k=1:length(explained)
	if sum(explained(1:k))>99
		ans=k;
		break;
	end
end
tran=coeff(:,1:ans);
featuresTrainTest_PCA= featuresTrainTest * tran;
featuresTrain_PCA=featuresTrainTest_PCA(1:numTrain,:);
featuresTest_PCA=featuresTrainTest_PCA((numTrain+1):(numTrain+numTest),:);
%仅仅取前k维向量
%tran=coeff(:,1:k);
% B=A*coeff;
% 
% % [coeff,latent,explained]=pcacov(featureTest);
%     
% %     %1设定方差贡献度为99%
% %     for i=1:length(explained)
% %         if sum(explained(1:i))>99
% %             ans=i;
% %             break;
% %         end
% %     end
% % tran=coeff(:,1:ans);
% % featureTest_PCA= featureTest * tran;
%     %仅仅取前k维向量
%     %tran=coeff(:,1:k);
%     % B=A*coeff;
    
    
% % train_PCA    未修改前
% featuresTrain = zscore(featuresTrain);
% [coeff,latent,explained]=pcacov(featuresTrain);
% 
% %1设定方差贡献度为99%
% for k=1:length(explained)
% 	if sum(explained(1:k))>99
% 		ans=k;
% 		break;
% 	end
% end
% tran=coeff(:,1:ans);
% featuresTrain_PCA= featuresTrain * tran;
% %仅仅取前k维向量
% %tran=coeff(:,1:k);
% % B=A*coeff;
% % test_PCA
% featureTest = zscore(featureTest);
% [coeff,latent,explained]=pcacov(featureTest);
%     
% %     %1设定方差贡献度为99%
% %     for i=1:length(explained)
% %         if sum(explained(1:i))>99
% %             ans=i;
% %             break;
% %         end
% %     end
% tran=coeff(:,1:ans);
% featureTest_PCA= featureTest * tran;
%     %仅仅取前k维向量
%     %tran=coeff(:,1:k);
%     % B=A*coeff;

    
% % 开始svm多分类训练，注意：fitcsvm用于二分类，fitcecoc用于多分类,1 VS 1方法   
% 所有训练图像标签    
% trainLabels = imdsTrain.Labels;  

% %高斯核函数的SVM分类
% t = templateSVM('Standardize',true,'KernelFunction','RBF');%改成RBF,效果不好
% classifer = fitcecoc(featuresTrain_PCA,trainLabels,'Learners',t);

classifer = fitcecoc(featuresTrain_PCA,TrainLabels);    % train_PCA
% classifer = fitcecoc(featuresTrain,trainLabels);

[predictIndex,score] = predict(classifer,featuresTest_PCA);  %pca，混淆矩阵

% %把predictIndex写成csv文件，但是报错（未定义与 'categorical' 类型的输入参数相对应的函数 'real'。），直接粘贴算了
% csvwrite('.\BS-SVM-predictIndex.csv',predictIndex)
% % 生成excel文件，还没调试代码
% xlswrite(filetitle,a);%生成文件名变化的xlsx文件
% %生成表格，按列生成，代码没调试
% result_table=table(m,A(:,1),A(:,2),A(:,3),'VariableNames',col);
% %保存表格
% writetable(result_table, 'test.csv');



% for i = 1:numTest   
%     featureTest_ppca = featureTest_PCA(i,:);    %pca
%     [predictIndex,score] = predict(classifer,featureTest_ppca);  %pca
    
%     [predictIndex,score] = predict(classifer,featureTest(i,:));  %无pca，单个提取featureTest(i,:)和predictIndex
%     TestLabels_cellstr = cellstr(TestLabels(i)); % categorica变cell
%     TestLabels_cellmat = cell2mat(TestLabels_cellstr);% cell变char
%     predictIndex = cellstr(predictIndex); % categorica变cell
%     predictIndex = cell2mat(predictIndex);% cell变char   
%     
%     if TestLabels_cellmat == predictIndex% 匹配字符char
%         acc = acc + 1;  % 总准确率
%         if predictIndex == '1'  % 各类准确率
%             acc1 = acc1 + 1;
%         elseif predictIndex == '2'  % 各类准确率
%             acc2 = acc2 + 1;
%         elseif predictIndex == '3'  % 各类准确率
%             acc3 = acc3 + 1;
%         elseif predictIndex == '4'  % 各类准确率
%             acc4 = acc4 + 1;
%         elseif predictIndex == '5'  % 各类准确率
%             acc5 = acc5 + 1;
%         else
%             acc6 = acc6 + 1;
%         end
%             
%     end
%     
% %     figure;imshow(testImage);    
% %     title(['predictImage: ',char(predictIndex)]);    
%  end
% totalacc = acc / numTest * 100;
% for i = 1:6     % 计算每一类的准确率
%     numTesti = Test_disp(i,2);% tabel变array数组
%     numTesti = table2array(numTesti); % 第i类个数
%     if i == 1  % 各类准确率
%             acci = acc1;
%     elseif i == 2  % 各类准确率
%             acci = acc2;
%     elseif i == 3  % 各类准确率
%             acci = acc3;
%     elseif i == 4  % 各类准确率
%             acci = acc4;
%     elseif i == 5  % 各类准确率
%             acci = acc5;
%     else
%             acci = acc6;
%     end
%     totalacci = acci / numTesti *100;% 第i类准确率
%     fprintf('第 %d 类的准确率是 %4.2f%% \n',i,totalacci);
% 
% end
% fprintf('总的准确率是 %4.2f %%\n',totalacc);

% % 混淆矩阵         %好像不能用，画出来的不对。
% % 绘制混淆矩阵plotconfusion(AA,BB);
% TestLabels_cellstr = cellstr(TestLabels); % categorica变cell
% TestLabels_cellmat = cell2mat(TestLabels_cellstr);% cell变char
% predictIndex_cellstr = cellstr(predictIndex); % categorica变cell
% predictIndex_cellmat = cell2mat(predictIndex_cellstr);% cell变char   
% TestLabels = imdsTest.Labels; 
% Test_Labels = double(TestLabels);
% predict_label = double(predictIndex);
% caTest_Labels = categorical(TestLabels);
% capredict_label = categorical(predictIndex);
% % % % plotconfusion(AA,BB);
% % % TestLabels = imdsTest.Labels; 
% % % Test_Labels = double(TestLabels);
% % % Test_Labels = Test_Labels'; 
% tabletest=countEachLabel(imdsTest);%这是个结构体，点开工作区的变量见名知意
% num_in_class=tabletest.Count';%这个num_in_class 和祖传代码等价，但这次是用程序自动完成的
% %num_in_class=[142,269,233,145,244,142,276,159]%这个是祖传代码更新后测试集的数据,用来画混淆矩阵
% classnames=cellstr(tabletest.Label);
% name_class=classnames';%是一个1xn的cell向量，绘制混淆矩阵需要用到
% % % predictlabel = (double(predictIndex)-1);
% % % predict_label = predictlabel';
% % % predict_label = double(predictIndex);
% % % predict_label = predict_label';
% [confusion_matrix]=compute_confusion_matrix(predict_label,Test_Labels,num_in_class,name_class);%绘制混淆矩阵，所以混淆矩阵的3个函数要放在同一个文件夹内
%%

% numTest0 = Test_disp(1,2);% tabel变array数组
% numTest0 = table2array(numTest0); % 第一类个数
% totalacc0 = acc0 / numTest0;% 第一类准确率

%% 如果没有测试集，则使用训练集看一下训练出来的SVM在训练集上的效果
% numTest = length(imdsTrain.Files);    
% for i = 1:numTest    
%     testImage = readimage(imdsTrain,i);    
%     scaleTestImage = imresize(testImage,imageSize);    
%     featureTest = extractHOGFeatures(scaleTestImage);    
%     [predictIndex,score] = predict(classifer,featureTest);    
%     figure;imshow(testImage);    
%     title(['predictImage: ',char(predictIndex)]);    
% end





    