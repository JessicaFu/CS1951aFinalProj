mean = 1430401868.5157232;
std = 297786.6319579399;
x = [1430401868.5157232 - 3*297786.6319579399:1:1430401868.5157232 + 3*297786.6319579399];
norm = normpdf(x,mean,std);

general = [1430404268.2336957, 293886.35314878455];
chronicle = [1430577365.7142856, 377694.60811073065];
huff = [1430408655.862069, 296911.3523516595];
bbc = [1430416842.3181818, 202783.01322604693];
al = [1430298984.8888888, 312854.0101848871];
cnn = [1430056500, 0];
herald = [1430209226.6666667, 147867.11361519466];
wash = [1430368762.2857144, 239207.00452101807];

figure;
title('Nepal Earthquake Article Probability');
xlabel('Time (seconds since time 0)');
ylabel('Probability of article appearing');
hold on;
plot(x,normpdf(x,general(1),general(2)));
plot(x,normpdf(x,chronicle(1),chronicle(2)));
plot(x,normpdf(x,huff(1),huff(2)));
plot(x,normpdf(x,bbc(1),bbc(2)));
plot(x,normpdf(x,al(1),al(2)));
plot(x,normpdf(x,cnn(1),cnn(2)));
plot(x,normpdf(x,herald(1),herald(2)));
plot(x,normpdf(x,wash(1),wash(2)));
legend('Aggregate','The Chronicle','Huffington Post','BBC','Al Jazeera','CNN','The Herald Sun','The Washington Post');