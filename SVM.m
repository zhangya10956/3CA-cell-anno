%% ���������Լ��ղŲ���HOG������һ�δ��룬ûʲô��
% %% ����HOG����
% clear all; close all; clc;
% img=imread('yangLi1.png');
% im=imresize(img,[64,64]);  
% % �����ǻҶ�ͼ�񣬾Ͳ���Ҫ��RGBת�ɻҶ���
% % img=rgb2gray(im);  
% % �����õ���MATLAB�Դ���HOG������ȡ������Ҳ��֪��ʲô��HOG���������ǿ����϶�ͼ����SVM����ʱ�����õ������������������
% [featureVector,hogVisualization] = extractHOGFeatures(im); 
% data(1,:)=featureVector;  
% imshow(im);
% hold on;
% plot(hogVisualization);




%% ��hog������ͼ����ж���࣬svmѵ����1 VS 1    
%% 1 ���ݼ�������ѵ���ĺͲ��Ե� (ע���Լ�ͼƬ���·��) 
% clear;
% imds = imageDatastore('F:\Dataset\ICPR_HEp2016',...    
%     'IncludeSubfolders',true,...    
%     'LabelSource','foldernames'); 
% 
% imds = shuffle(imds);% ��������˳��
% [imdsTrain,imdsTest] = splitEachLabel(imds,0.8,0.2);% �������ݼ�
imdsTrain = imageDatastore('D:\PyCharm Community Edition 2021.2.3\dataset\DBSY\scMRA\10X-Smart\Trachea\0415-concat-1-HVG2000\train',...             %ֱ�Ӹ���·��������
    'IncludeSubfolders',true,...    
    'LabelSource','foldernames');   
imdsTrain = shuffle(imdsTrain);% ��������˳��


% ��֪������û�в��Լ�������в��Լ�������Ҫ��������д���
% ���û�в��Լ�������ʹ��ѵ������һ����ѵ�����ϵ�Ч����
% ����������ԵĻ������Խ������ѵ������֣�splitEachLabel�����������ã�������Ҳû�ù������Բο�һ��

imdsTest = imageDatastore('D:\PyCharm Community Edition 2021.2.3\dataset\DBSY\scMRA\10X-Smart\Trachea\0415-concat-1-HVG2000\test',...                %ֱ�Ӹ���·��������
    'IncludeSubfolders',true,...    
    'LabelSource','foldernames');    
  
  
%% ��ʾѵ����ͼƬ����Labels������Count  
numTrain = length(imdsTrain.Files); 
Train_disp = countEachLabel(imdsTrain);  
TrainLabels = imdsTrain.Labels;
disp(Train_disp);  
    


%% Ԥ�Ⲣ��ʾԤ��Ч��ͼ 
% ����в��Լ�����������һ�Σ�
numTest = length(imdsTest.Files);  
% featureTest1 = zeros(numTest,size(lbpFeaturestrain,2),'single');
% featureTest2 = zeros(numTest,size(hogfeaturestrain,2),'single');
% featureTest = zeros(numTest,size(features,2),'single');
% testimage1 = readimage(imdsTest,1);    
% scaleImagetesttest = imresize(testimage1,imageSize); 
% ���в���ͼ���ǩ 
Test_disp = countEachLabel(imdsTest);
TestLabels = imdsTest.Labels; 

% acc = 0;
% acc1 = 0;
% acc2 = 0;
% acc3 = 0;
% acc4 = 0;
% acc5 = 0;
% acc6 = 0;
%featuresTest1��LBP����
% lbpFeaturestest = extractLBPFeatures(scaleImagetesttest,'CellSize',[lbp_CellSize lbp_CellSize],'Normalization',Normalization,'Upright',Upright);
% featuresTest1 = zeros(numTest,size(lbpFeaturestest,2),'single'); % featuresTest1Ϊ˫���ȣ���Ȼ�ᱨ��
%featuresTest2��HOG����
% [hogfeaturestest,visualization] = extractHOGFeatures(scaleImagetesttest);
% 'CellSize',[hog_CellSize hog_CellSize],'BlockSize',[hog_BlockSize hog_BlockSize],'NumBins',NumBins);
% featuresTest2 = zeros(numTest,size(hogfeaturestest,2),'single'); % featuresTest1Ϊ˫���ȣ���Ȼ�ᱨ��






% train_PCA
% featuresTrain = zscore(imdsTrain);
featuresTrain = zeros(numTrain:2000);
% % ϡ�����
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
% % �ܵ�featuresTest���ڴ治��
featuresTest = zeros(5705:2000);        %ԭ����zeros(numTest;:2000);     numTestʱ��ʾ�ڴ治�������ǲ�����
% ϡ�����
% featuresTest = sparse(numTest:2000);
for iii=1:numTest
    testImage = readimage(imdsTest,iii);
    testImage = reshape(testImage,1,2000);    
    featuresTest(iii,:) = testImage;
end

featuresTest = zscore(featuresTest);





% % �ֵ�featuresTest
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
% % % �ֵ�featuresTest





featuresTrainTest = [featuresTrain;featuresTest];

[coeff,latent,explained]=pcacov(featuresTrainTest);

%1�趨����׶�Ϊ99%
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
%����ȡǰkά����
%tran=coeff(:,1:k);
% B=A*coeff;
% 
% % [coeff,latent,explained]=pcacov(featureTest);
%     
% %     %1�趨����׶�Ϊ99%
% %     for i=1:length(explained)
% %         if sum(explained(1:i))>99
% %             ans=i;
% %             break;
% %         end
% %     end
% % tran=coeff(:,1:ans);
% % featureTest_PCA= featureTest * tran;
%     %����ȡǰkά����
%     %tran=coeff(:,1:k);
%     % B=A*coeff;
    
    
% % train_PCA    δ�޸�ǰ
% featuresTrain = zscore(featuresTrain);
% [coeff,latent,explained]=pcacov(featuresTrain);
% 
% %1�趨����׶�Ϊ99%
% for k=1:length(explained)
% 	if sum(explained(1:k))>99
% 		ans=k;
% 		break;
% 	end
% end
% tran=coeff(:,1:ans);
% featuresTrain_PCA= featuresTrain * tran;
% %����ȡǰkά����
% %tran=coeff(:,1:k);
% % B=A*coeff;
% % test_PCA
% featureTest = zscore(featureTest);
% [coeff,latent,explained]=pcacov(featureTest);
%     
% %     %1�趨����׶�Ϊ99%
% %     for i=1:length(explained)
% %         if sum(explained(1:i))>99
% %             ans=i;
% %             break;
% %         end
% %     end
% tran=coeff(:,1:ans);
% featureTest_PCA= featureTest * tran;
%     %����ȡǰkά����
%     %tran=coeff(:,1:k);
%     % B=A*coeff;

    
% % ��ʼsvm�����ѵ����ע�⣺fitcsvm���ڶ����࣬fitcecoc���ڶ����,1 VS 1����   
% ����ѵ��ͼ���ǩ    
% trainLabels = imdsTrain.Labels;  

% %��˹�˺�����SVM����
% t = templateSVM('Standardize',true,'KernelFunction','RBF');%�ĳ�RBF,Ч������
% classifer = fitcecoc(featuresTrain_PCA,trainLabels,'Learners',t);

classifer = fitcecoc(featuresTrain_PCA,TrainLabels);    % train_PCA
% classifer = fitcecoc(featuresTrain,trainLabels);

[predictIndex,score] = predict(classifer,featuresTest_PCA);  %pca����������

% %��predictIndexд��csv�ļ������Ǳ���δ������ 'categorical' ���͵�����������Ӧ�ĺ��� 'real'������ֱ��ճ������
% csvwrite('.\BS-SVM-predictIndex.csv',predictIndex)
% % ����excel�ļ�����û���Դ���
% xlswrite(filetitle,a);%�����ļ����仯��xlsx�ļ�
% %���ɱ�񣬰������ɣ�����û����
% result_table=table(m,A(:,1),A(:,2),A(:,3),'VariableNames',col);
% %������
% writetable(result_table, 'test.csv');



% for i = 1:numTest   
%     featureTest_ppca = featureTest_PCA(i,:);    %pca
%     [predictIndex,score] = predict(classifer,featureTest_ppca);  %pca
    
%     [predictIndex,score] = predict(classifer,featureTest(i,:));  %��pca��������ȡfeatureTest(i,:)��predictIndex
%     TestLabels_cellstr = cellstr(TestLabels(i)); % categorica��cell
%     TestLabels_cellmat = cell2mat(TestLabels_cellstr);% cell��char
%     predictIndex = cellstr(predictIndex); % categorica��cell
%     predictIndex = cell2mat(predictIndex);% cell��char   
%     
%     if TestLabels_cellmat == predictIndex% ƥ���ַ�char
%         acc = acc + 1;  % ��׼ȷ��
%         if predictIndex == '1'  % ����׼ȷ��
%             acc1 = acc1 + 1;
%         elseif predictIndex == '2'  % ����׼ȷ��
%             acc2 = acc2 + 1;
%         elseif predictIndex == '3'  % ����׼ȷ��
%             acc3 = acc3 + 1;
%         elseif predictIndex == '4'  % ����׼ȷ��
%             acc4 = acc4 + 1;
%         elseif predictIndex == '5'  % ����׼ȷ��
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
% for i = 1:6     % ����ÿһ���׼ȷ��
%     numTesti = Test_disp(i,2);% tabel��array����
%     numTesti = table2array(numTesti); % ��i�����
%     if i == 1  % ����׼ȷ��
%             acci = acc1;
%     elseif i == 2  % ����׼ȷ��
%             acci = acc2;
%     elseif i == 3  % ����׼ȷ��
%             acci = acc3;
%     elseif i == 4  % ����׼ȷ��
%             acci = acc4;
%     elseif i == 5  % ����׼ȷ��
%             acci = acc5;
%     else
%             acci = acc6;
%     end
%     totalacci = acci / numTesti *100;% ��i��׼ȷ��
%     fprintf('�� %d ���׼ȷ���� %4.2f%% \n',i,totalacci);
% 
% end
% fprintf('�ܵ�׼ȷ���� %4.2f %%\n',totalacc);

% % ��������         %�������ã��������Ĳ��ԡ�
% % ���ƻ�������plotconfusion(AA,BB);
% TestLabels_cellstr = cellstr(TestLabels); % categorica��cell
% TestLabels_cellmat = cell2mat(TestLabels_cellstr);% cell��char
% predictIndex_cellstr = cellstr(predictIndex); % categorica��cell
% predictIndex_cellmat = cell2mat(predictIndex_cellstr);% cell��char   
% TestLabels = imdsTest.Labels; 
% Test_Labels = double(TestLabels);
% predict_label = double(predictIndex);
% caTest_Labels = categorical(TestLabels);
% capredict_label = categorical(predictIndex);
% % % % plotconfusion(AA,BB);
% % % TestLabels = imdsTest.Labels; 
% % % Test_Labels = double(TestLabels);
% % % Test_Labels = Test_Labels'; 
% tabletest=countEachLabel(imdsTest);%���Ǹ��ṹ�壬�㿪�������ı�������֪��
% num_in_class=tabletest.Count';%���num_in_class ���洫����ȼۣ���������ó����Զ���ɵ�
% %num_in_class=[142,269,233,145,244,142,276,159]%������洫������º���Լ�������,��������������
% classnames=cellstr(tabletest.Label);
% name_class=classnames';%��һ��1xn��cell���������ƻ���������Ҫ�õ�
% % % predictlabel = (double(predictIndex)-1);
% % % predict_label = predictlabel';
% % % predict_label = double(predictIndex);
% % % predict_label = predict_label';
% [confusion_matrix]=compute_confusion_matrix(predict_label,Test_Labels,num_in_class,name_class);%���ƻ����������Ի��������3������Ҫ����ͬһ���ļ�����
%%

% numTest0 = Test_disp(1,2);% tabel��array����
% numTest0 = table2array(numTest0); % ��һ�����
% totalacc0 = acc0 / numTest0;% ��һ��׼ȷ��

%% ���û�в��Լ�����ʹ��ѵ������һ��ѵ��������SVM��ѵ�����ϵ�Ч��
% numTest = length(imdsTrain.Files);    
% for i = 1:numTest    
%     testImage = readimage(imdsTrain,i);    
%     scaleTestImage = imresize(testImage,imageSize);    
%     featureTest = extractHOGFeatures(scaleTestImage);    
%     [predictIndex,score] = predict(classifer,featureTest);    
%     figure;imshow(testImage);    
%     title(['predictImage: ',char(predictIndex)]);    
% end





    