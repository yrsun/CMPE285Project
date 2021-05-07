# CMPE285Project

TEST CASE:
1. Strategies or strategy are selected. Enter an investment value that is less than 5000 should display an error page ✓
2. Strategies or strategy are selected. Enter an investment value with characters other than 0~9 or leave empty, should display an error page ✓
3. Did not select any strategy. Did not enter any investment value from home page, but click submit, should display an error page ✓
4. Enter an investment value without selecting any strategy from home page should display an error page ✓
5. Select 'ethical' strategy and enter 5000, click submit, display stock portfolio 
6. Select 'index' and 'quality' strategies and enter 5000, click submit, display stock portfolio
7. Select 'index' and 'index' strategies and enter 5000, click submit, should display an error page ✓


-------------------------------------------------------------------------------------------------------
# 任务详情（临时文件）

## 项目实现：
### 1. 使用流程：
输入金额 
选择Investing strategy 
显示结果

## 项目方式：
1. strategy内的股票是自定义还是手动指定? 

3. How stocks/ETFs are mapped to investing strategy？

5. How the money is divided among buying？

7. How to present the weekly history of the portfolio value？

9. How many extra feature should be implemented to improve the project？

11. 结果输出样式

## 项目文件结构
### py文件定义
app.py：
function.py:

### 函数定义
getStock(s1, s2)
注释说明（函数说明加参数说明）：


getStockInfo(stock)
注释说明：

getStockClose(stocks, stocksInfo)
注释说明：

generateBarChart(stocks, stocksInfo)
注释说明：

generateProfitChart(value, stocks, stocksInfo)
注释说明：

generateStocksInfo(stocks, stocksInfo, value)
注释说明：

generatePortfolio()
注释说明：

## Flask实现方式：

## 前端连接：

