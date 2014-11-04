//
//  main.cpp
//  sort
//
//  Created by Xiaoying Wang on 14-7-14.
//  Copyright (c) 2014年 edu.tongji. All rights reserved.
//

#include <iostream>
#include <vector>
#include <cstring>
#include <ctime>

using namespace std;

enum COMAND_CHOOSE{
    BUBBLE_SORT,
    SELECTION_SORT,
    INSERTON_SORT,
    SHELL_SORT,
    QUICK_SORT,
    HEAP_SORT,
    MERGE_SORT,
    RADIX_SORT,
    RESTART,
    QUIT
};


void getRandomNumbers(vector<int> &origin, int length){                    //得到原始随机数列
    for(int i = 0; i < length; ++i){
        origin.push_back(rand()%length);
    }
}

void getNumberList(vector<int> &origin){                                    //输入想要的数列长度并得到数列
    cout<<"请输入要产生的随机数的个数：";
    string s_length;
    cin>>s_length;                          //防止恶意输入
    int length = atoi(s_length.c_str());    //得到随机数个数
    while(length <= 0){
        cout<<"输入数字不在要求范围内，请重新输入：";
        cin>>length;
    }
    getRandomNumbers(origin, length);
}


void output(double time, int count, int CMD){         //输出本次排序结果
    bool flag = true;
    
    switch(CMD){
        case BUBBLE_SORT: cout<<"------冒泡排序------"<<endl; break;
        case SELECTION_SORT: cout<<"------选择排序------"<<endl; break;
        case INSERTON_SORT: cout<<"------插入排序------"<<endl; break;
        case SHELL_SORT: cout<<"------希尔排序------"<<endl; break;
        case QUICK_SORT: cout<<"------快速排序------"<<endl; break;
        case HEAP_SORT: cout<<"------堆排序------"<<endl; break;
        case MERGE_SORT: cout<<"------归并排序------"<<endl; break;
        case RADIX_SORT: cout<<"------基数排序------"<<endl; break;
        default: flag = false; break;
    }
    
    if(!flag) return;                       //输入命令不存在，重新输入
    
    cout<<"所用时间：    "<<time<<" 秒"<<endl;
    cout<<"交换次数：    "<<count<<" 次"<<endl;

}

//void showSorted(vector<int> &sorted){                  //检查结果，调试用
//    for(int i = 0; i < sorted.size(); ++i){
//        cout<<sorted[i]<<" ";
//    }
//    cout<<endl;
//}

/***************************************冒泡排序***************************************/

void bubbleSort(vector<int> &copy, int &count){                         //冒泡排序
    for(int i = 0; i < copy.size()-1; ++i){
        bool flag = true;
        for(int j = 0; j < copy.size()-1-i; ++j){
            if(copy[j] > copy[j+1]){
                swap(copy[j], copy[j+1]);
                count++;
                flag = false;
            }
        }
        if(flag) break;                     //简单优化
    }
}

void bubbleSortAd(int copy[], int size){            //优化
    int flag = size;
    for(int i = 0; i < flag; ++i){
        int k = flag;
        for(int j = 0; j < flag-1; ++j){
            if(copy[j] > copy[j+1]){
                swap(copy[j], copy[j+1]);
                k = j+1;
            }
        }
        flag = k;
    }
}

/***************************************选择排序***************************************/

void selectionSort(vector<int> &copy, int &count){                     //选择排序
    for(int i = 0; i < copy.size()-1; ++i){
        int min_index = i;
        for(int j = i+1; j <copy.size(); ++j){
            if(copy[j] < copy[min_index]) min_index = j;
        }
        if(i != min_index){
            swap(copy[i],copy[min_index]);
            count++;
        }
    }
}

/***************************************插入排序***************************************/

void insertionSort(vector<int> &copy, int &count){                     //插入排序
    for(int i = 1; i < copy.size(); ++i){
        int tmp = copy[i];
        bool flag = true;
        for(int j = i-1; j >= 0; --j){
            if(copy[j] > tmp){
                copy[j+1] = copy[j];
                count++;
            }else{
                copy[j+1] = tmp;
                flag = false;
                break;
            }
        }
        if(flag) copy[0] = tmp;
    }
}

/***************************************希尔排序***************************************/

void sortGroup(vector<int> &copy, int begin, int n_step, int &count){   //分别给对每组进行插入排序
    for(int i = begin+n_step; i < copy.size(); i += n_step){
        int tmp = copy[i];
        bool flag = true;
        for(int j = i-n_step; j >= 0; j -= n_step){
            if(copy[j] > tmp){
                copy[j+n_step] = copy[j];
                count++;
            }else{
                copy[j+n_step] = tmp;
                flag = false;
                break;
            }
        }
        if(flag) copy[begin] = tmp;
    }
}

void shellSort(vector<int> &copy, int &count){                         //希尔排序
    int n_step = (int)copy.size()/2;
    for(; n_step > 0; n_step /= 2){
        for(int i = 0; i < n_step; ++i){
            sortGroup(copy, i, n_step, count);
        }
    }
}

/***************************************快速排序***************************************/

void quickSort(vector<int> &copy, int p, int q, int &count){           //快速排序
    int mid_number = copy[(p+q)>>1];
    int i = p, j = q;
    while(i <= j){
        while(copy[i] < mid_number) ++i;
        while(copy[j] > mid_number) --j;
        if(i <= j){
            swap(copy[i], copy[j]);
            ++i;
            --j;
            count++;
        }
    }
    if(i < q) quickSort(copy, i, q, count);
    if(j > p) quickSort(copy, p, j, count);
}

/***************************************堆排序***************************************/

void heapDown(vector<int> &copy, int heap_size, int sort_pos, int &count){    //调整当前节点，使其满足堆的性质
    while(2*sort_pos+1 < heap_size){
        int max_pos = 2*sort_pos + 1;
        if(max_pos+1 < heap_size && copy[max_pos] < copy[max_pos+1]){
            max_pos += 1;
        }
        if(copy[sort_pos] > copy[max_pos]) break;
        else{
            swap(copy[sort_pos], copy[max_pos]);
            sort_pos = max_pos;
            count++;
        }
    }
}

void heapSort(vector<int> &copy, int &count){                           //堆排序
    int heap_size = (int)copy.size();
    for(int i = heap_size/2 - 1; i >= 0; --i){          //创建堆
        heapDown(copy, heap_size, i, count);
    }
    for(; heap_size > 1; --heap_size){               //排数列
        swap(copy[0], copy[heap_size-1]);
        count++;
        heapDown(copy, heap_size-1, 0, count);
    }
}

/***************************************归并排序***************************************/

void merge(vector<int> &copy, vector<int> &copy_a, vector<int> &copy_b, int &count){    //合并两个数列
    int i = 0, j = 0, k = 0;
    while(i < copy_a.size() && j < copy_b.size()){
        if(copy_a[i] <= copy_b[j]) copy[k] = copy_a[i++];
        else{
            copy[k] = copy_b[j++];
            count++;
        }
        k++;
    }
    if(copy_a.size() == i){
        for(; k < copy.size(); ++k){
            copy[k] = copy_b[j++];
        }
    }else{
        for(; k < copy.size();++k){
            copy[k] = copy_a[i++];
            count++;
        }
    }
}

void mergeSort(vector<int> &copy, int &count){                         //归并排序
    if(copy.size() <= 1) return;
    int mid_pos = (int)copy.size()/2;
    vector<int> copy_a(copy.begin(), copy.begin()+mid_pos);
    vector<int> copy_b(copy.begin()+mid_pos, copy.end());
    mergeSort(copy_a, count);
    mergeSort(copy_b, count);
    merge(copy,copy_a,copy_b, count);
}

/***************************************基数排序***************************************/

void radixSort(vector<int> &copy){                                      //基数排序
    int max_num = copy[0];
    for(int i = 1; i < copy.size(); ++i){
        if(copy[i] > max_num) max_num = copy[i];
    }
    int num_length = 0;                             //最大数的位数
    while(max_num > 0){
        num_length++;
        max_num /= 10;
    }
    
    vector<vector<int>> buckets;                    //创建10个桶
    for(int i = 0; i < 10; ++i){
        vector<int> new_vec;
        buckets.push_back(new_vec);
    }
    
    int radix = 1;
    for(int i = 0; i < num_length; ++i){
        for(int j = 0; j < copy.size(); ++j){
            int index = (copy[j] / radix) % 10;
            buckets[index].push_back(copy[j]);
        }
        copy.clear();
        for(int i = 0; i < 10; ++i){                    //分放入桶
            for(int j = 0; j < buckets[i].size(); ++j){
                copy.push_back(buckets[i][j]);
            }
        }
        for(int i = 0; i < 10; ++i){                    //回收
            buckets[i].clear();
        }
        radix *= 10;
    }
}                                                   //注：基数排序无交换次数




int main(int argc, const char * argv[])
{
    vector<int> origin;
    
    getNumberList(origin);
    
    bool flag = true;               //判断是否结束程序
    int command;                    //存放命令
    string s_cmd;
    
//    showSorted(origin);
    
    cout<<"----------------------------------------------"<<endl;
    cout<<"                   排序算法比较                 "<<endl;
    cout<<"----------------------------------------------"<<endl;
    cout<<"                 0 ------ 冒泡排序             "<<endl;
    cout<<"                 1 ------ 选择排序             "<<endl;
    cout<<"                 2 ------ 插入排序             "<<endl;
    cout<<"                 3 ------ 希尔排序             "<<endl;
    cout<<"                 4 ------ 快速排序             "<<endl;
    cout<<"                 5 ------  堆排序              "<<endl;
    cout<<"                 6 ------ 归并排序             "<<endl;
    cout<<"                 7 ------ 基数排序             "<<endl;
    cout<<"                 8 ------ 重新生成             "<<endl;
    cout<<"                 9 ------ 退出程序             "<<endl;
    cout<<"----------------------------------------------"<<endl<<endl;
    
    while(true){
        vector<int> copy(origin);
        cout<<"请选择运行命令：";
        cin>>s_cmd;
        command = s_cmd[0] - '0';               //防止恶意输入
        
        clock_t start = clock();                //开始计时
        
        int count = 0;                          //交换次数
        
        switch(command){
            case BUBBLE_SORT: bubbleSort(copy, count); break;                           //输入：0
            case SELECTION_SORT: selectionSort(copy, count); break;                     //输入：1
            case INSERTON_SORT: insertionSort(copy, count); break;                      //输入：2
            case SHELL_SORT: shellSort(copy, count); break;                             //输入：3
            case QUICK_SORT: quickSort(copy, 0, (int)origin.size()-1, count); break;    //输入：4
            case HEAP_SORT: heapSort(copy, count); break;                               //输入：5
            case MERGE_SORT: mergeSort(copy, count); break;                             //输入：6
            case RADIX_SORT: radixSort(copy); break;                                    //输入：7
            case RESTART: origin.clear(); getNumberList(origin); break;                 //输入：8
            case QUIT: flag = false; break;                                             //输入：9
            default: cout<<"不存在该选项，请输入数字0 ~ 9"<<endl; break;                    //输入：其它
        }
        
        if(!flag) break;                        //退出
        if(RESTART == command) continue;
        
        clock_t finish = clock();               //结束计时
        
        double total = (double)(finish-start)/CLOCKS_PER_SEC;   //总计时
        
        output(total, count, command);
        
//        showSorted(copy);
    }
        
        
    
    return 0;
}