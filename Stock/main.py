import pandas as pd
import os
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PanelOLS


if __name__ == "__main__":
    
    chinafin_dir = 'Stock/chinafin_csv'
    cntop10_dir = 'Stock/cntop10_csv'

    calc_mat = np.zeros([50, 5])

    # 计算总资产收益率 TDA LDA SIZE ROE
    file_list = os.listdir(chinafin_dir)

    loop_count = 0
    for each_file in file_list:
        data = pd.read_csv(chinafin_dir + '/' + each_file,
                        usecols=[35, 58, 68, 132])
        series = data.iloc[-1:]
        total_asset, total_debt, pure_asset, pure_profit = series['A033'], series[
            'A056'], series['A066'], series['P022']
        calc_mat[loop_count, 0] = pure_profit / total_asset
        calc_mat[loop_count, 1] = total_debt / total_asset
        calc_mat[loop_count, 3] = np.log(total_asset)
        calc_mat[loop_count, 4] = pure_profit / pure_asset
        loop_count += 1
        # total_asset_ratio = pure_profit / total_asset
        # TD_A =  total_debt / total_asset
        # LD_A = long_debt / total_asset
        # ROE = pure_profit / pure_asset

    # 计算CR5
    file_list = os.listdir(cntop10_dir)

    loop_count = 0
    for each_file in file_list:
        data = pd.read_csv(cntop10_dir + '/' + each_file, usecols=[5])
        series = data.iloc[-10:-5, :]
        series = series.values.flatten()
        calc_mat[loop_count, 2] = np.sum(series)
        # CR5
        loop_count += 1

    # 计算描述性指标
    res_mat = np.zeros([5, 4])  #列为min max mean std
    for i in range(calc_mat.shape[1]):
        series = calc_mat[:, i]
        res_mat[i, 0] = np.min(series)
        res_mat[i, 1] = np.max(series)
        res_mat[i, 2] = np.mean(series)
        res_mat[i, 3] = np.std(series)

    np.savetxt('Stock/stats.txt', res_mat, delimiter=',')

    # 计算皮尔逊相关系数
    pearson_mat = np.zeros([5, 5])  # 总资产收益率 TDA CR5 SIZE ORE
    for i in range(pearson_mat.shape[0]):
        for j in range(pearson_mat.shape[0]):
            if i == j:
                pearson_mat[i, j] = 1
                continue
            series_i, series_j = calc_mat[:, i], calc_mat[:, j]
            mean_i, mean_j = res_mat[i, 2], res_mat[j, 2]
            std_i, std_j = res_mat[i, 3], res_mat[j, 3]
            coeff = 0
            for k in range(len(series_i)):
                coeff += (series_i[k] - mean_i) * (series_j[k] - mean_j)
            coeff /= (std_i * std_j)
            pearson_mat[i, j] = coeff

    np.savetxt('Stock/pearson.txt', pearson_mat, delimiter=',')

    # 多元OLS回归
    y = calc_mat[:, 0]
    x = np.stack([calc_mat[:, 1], calc_mat[:, 2], calc_mat[:, 3], calc_mat[:, 4]])
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for elem in x[1:]:
        X = sm.add_constant(np.column_stack((elem, X)))
    res = sm.OLS(y,X).fit()
    print(res.summary())

    FE模型回归
    company_codes = []
    for each_file in file_list:
        company_code = each_file.split('.')[0]
        company_code = int(company_code)
        company_codes.append(company_code)
    time = [2019] * 50
    df = pd.DataFrame({
        'TDA': x[0],
        'CR5': x[1],
        'SIZE': x[2],
        'ROE': x[3],
        'REWARD': y,
        'YEAR': time,
        'CODE': company_codes
    })
    df.to_stata('Stock/res.dta')
    df = df.set_index(['CODE', 'YEAR'])
    exog_vars = ['TDA', 'LDA', 'SIZE', 'ROE']
    exog = sm.add_constant(df[exog_vars])
    model = PanelOLS(df['REWARD'], exog, entity_effects=True)
    fe = model.fit()
    print(fe)