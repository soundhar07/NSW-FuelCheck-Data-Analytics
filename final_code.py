#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Third-party libraries
# NOTE: You may **only** use the following third-party libraries:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# NOTE: It isn't necessary to use all of these to complete the assignment,
# but you are free to do so, should you choose.

# Standard libraries
# NOTE: You may use **any** of the Python 3.11 or 3.13 standard libraries:
# https://docs.python.org/3.11/library/index.html
# https://docs.python.org/3.13/library/index.html
from pathlib import Path

# ... import your standard libraries here ...


######################################################
# NOTE: DO NOT MODIFY THE LINE BELOW ...
######################################################
studentid = Path(__file__).stem


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION BELOW ...
######################################################
def log(question, output_df=None, other=None):
    print(f"--------------- {question}----------------")

    if other is not None:
        print(question, other)
    if output_df is not None:
        df = output_df.head(5).copy(True)
        for c in df.columns:
            df[c] = df[c].apply(lambda a: a[:20] if isinstance(a, str) else a)

        df.columns = [a[:10] + "..." for a in df.columns]
        print(df.to_string())


######################################################
# NOTE: YOU MAY ADD ANY HELPER FUNCTIONS BELOW ...
######################################################


######################################################
# QUESTIONS TO COMPLETE BELOW ...
######################################################


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_1(fuel_csv):
    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    dtype_mapper={
        'ServiceStationName': 'string',
        'Address': 'string',
        'Suburb': 'string',
        'Postcode': 'int64',
        'Brand': 'string',
        'FuelCode': 'string',
        'PriceUpdatedDate': 'string',
        'Price': 'float'
    }
    df1 = pd.read_csv('fuel.csv',quotechar='"',quoting=1,on_bad_lines= lambda x:x[1:],dtype = dtype_mapper,engine='python')
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 1", output_df=df1, other=df1.shape)
    return df1


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_2(df1):
    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    def remove_non_nsw(address):
        address = address.lower()
        if ('new south wales' in address or 'nsw' in address):
            return True
        return False
    df1 = df1.rename(columns={"ServiceStationName": "Name"})
    df1.Suburb = df1.Suburb.str.upper()
    df2=df1[df1.Address.apply(remove_non_nsw)]
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 2", output_df=df2, other=df2.shape)
    return df2


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_3(postcodes_json):
    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    pc_mapper={
    'postcode':'int64',
    'place_name':'string',
    'state_name':'string',
    'state_code':'string',
    'latitude':'float64',
    'longitude':'float64'
    }
    df3 = pd.read_json('postcodes.json',dtype=pc_mapper).drop('accuracy', axis=1)
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 3", output_df=df3, other=df3.shape)
    return df3


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_4(df2, df3):
    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    df3 = df3.rename(columns={"place_name": "Suburb","postcode":"Postcode","latitude":"Latitude","longitude":"Longitude"})
    df3.Suburb = df3.Suburb.str.upper()
    nsw_codes = df3[df3.state_code == 'NSW']
    columns=['Name','Address','Suburb','Postcode','Brand','FuelCode','PriceUpdatedDate','Price','Latitude','Longitude']
    merged_df1 = df2.merge(nsw_codes,on=['Postcode','Suburb'],how='left')
    merged_df1 = merged_df1[columns]
    not_merged_df1 = merged_df1[merged_df1.isnull().any(axis=1)]
    merged_df1 = merged_df1.dropna()
    nsw_codes=nsw_codes.sort_values(by=['Postcode','Suburb'])
    filtered_nsw_codes=nsw_codes.drop_duplicates(subset=['Postcode'])
    filtered_nsw_codes =filtered_nsw_codes[['Postcode','Latitude','Longitude']]
    not_merged_df1 = not_merged_df1 [['Name','Address','Suburb','Postcode','Brand','FuelCode','PriceUpdatedDate','Price']]
    merged_df2 = not_merged_df1.merge(filtered_nsw_codes, on = 'Postcode',how='left')
    df4 = pd.concat([merged_df1,merged_df2])
    df4.to_csv('df4.csv', index=False)
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 4", output_df=df4, other=df4.shape)
    return df4


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_5(df4):
    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    pf=df4.copy()
    def truncate_date(x):
        y=x.split(' ')
        return y[0]
    pf['PriceUpdatedDate']= pf['PriceUpdatedDate'].apply(truncate_date)
    daily_station_df=pf.groupby(['Name','FuelCode','PriceUpdatedDate']).agg({'Price': 'mean','Postcode': 'first'}).round(2)
    daily_postcode_df=daily_station_df.groupby(['Postcode','FuelCode','PriceUpdatedDate']).agg({'Price': 'mean'}).round(2)
    avg_postcode_df=daily_postcode_df.groupby(['Postcode','FuelCode']).agg({'Price': 'mean',}).round(2)
    postcode_fuelType = pd.MultiIndex.from_product([pf['Postcode'].unique(), pf['FuelCode'].unique()],names=['Postcode', 'FuelType'])
    df5=avg_postcode_df.reindex(postcode_fuelType , fill_value=0).reset_index()
    df5=df5.sort_values(by=['Postcode','FuelType']).set_index(['Postcode','FuelType'])
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 5", output_df=df5, other=df5.shape)
    return df5


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_6(df4, df5):
    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    redf4 =df4.rename(columns={'FuelCode':'FuelType'})
    result = pd.merge(redf4, df5, on=['Postcode','FuelType'], suffixes=('', '_avg'))
    result ['PriceChangeAverage'] = (((result.Price - result.Price_avg)/result.Price)*100).round(2)
    df6=result.drop('Price_avg',axis=1)
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 6", output_df=df6, other=df6.shape)
    return df6


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_7(df6):
    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    inter_df7=df6.copy()
    inter_df7['PriceChangePrevious'] = inter_df7.groupby(['Name', 'FuelType'])['Price'].diff().fillna(0).round(2)
    df7=inter_df7
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 7", output_df=df7, other=df7.shape)
    return df7


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_8(df7):
    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    df8=df7.copy()
    def truncate_date(x):
        y=x.split(' ')
        return y[0]

    # The average per-brand and per-type daily fuel price, where there may be multiple fuel readings per day 
    # for a particular fuel type and brand, which are now aggregated to the brand level.
    daily_brand_average_df = df8.groupby(['Brand','FuelType','PriceUpdatedDate']).agg({'Price': 'mean'}).round(2)

    # The final average per-brand and per-type fuel price,where the daily averages for each brand and fuel type 
    #are now aggregated to a single value covering the duration of the dataset.
    brand_average_df = daily_brand_average_df.groupby(['Brand','FuelType']).agg({'Price': 'mean'}).round(2)
    brand_fuelType = pd.MultiIndex.from_product([df8['Brand'].unique(), df8['FuelType'].unique()],names=['Brand', 'FuelType'])

    # Final average per-brand and per-type fuel
    brand_avg_df=brand_average_df .reindex(brand_fuelType).reset_index()
    
    # Extracted the brand which sells the minimum price for that particular fuel type.
    min_price_idx=brand_avg_df.groupby('FuelType')['Price'].idxmin()
    min_fuel_df = brand_avg_df.loc[min_price_idx]
    independent_avg_df = brand_avg_df[brand_avg_df['Brand']=='Independent']

    # Light shades for Independent and Dark Shades for Brand Stores
    fuel_colors = {
    "DL": ("#1f77b4", "#aec7e8"),   # Blue shades
    "E10": ("#2ca02c", "#98df8a"),  # Green shades
    "E85": ("#d62728", "#ff9896"),  # Red shades
    "LPG": ("#9467bd", "#c5b0d5"),  # Purple shades
    "P95": ("#8c564b", "#c49c94"),  # Brown shades
    "P98": ("#e377c2", "#f7b6d2"),  # Pink shades
    "PDL": ("#7f7f7f", "#c7c7c7"),  # Gray shades
    "U91": ("#bcbd22", "#dbdb8d")   # Yellow shades
    }
    merged_df = min_fuel_df.merge(independent_avg_df, on="FuelType", suffixes=("_Other", "_Independent"))
    merged_df = merged_df.sort_values("FuelType")
    x = np.arange(len(merged_df))  
    width = 0.35  

    fig, ax = plt.subplots(figsize=(11,8))
    bars1 = []
    bars2 = []
    for i, fuel in enumerate(merged_df["FuelType"]):
        color_other, color_independent = fuel_colors.get(fuel, ("#333333", "#999999"))  
        bars1.append(ax.bar(x[i] - width/2, merged_df.loc[i, "Price_Other"], width, color=color_other, label="Other Stores" if i == 0 else ""))
        bars2.append(ax.bar(x[i] + width/2, merged_df.loc[i, "Price_Independent"], width, color=color_independent, label="Independent" if i == 0 else ""))

    # Adding text labels (Brand Names) on bars
    for bar, brand in zip(bars1, merged_df["Brand_Other"]):
        ax.text(bar[0].get_x() + bar[0].get_width()/2, bar[0].get_height()+1, brand, ha='center', va='bottom', fontsize=7, rotation=90)

    for bar, brand in zip(bars2, merged_df["Brand_Independent"]):
        ax.text(bar[0].get_x() + bar[0].get_width()/2, bar[0].get_height()+1, brand, ha='center', va='bottom', fontsize=7, rotation=90)

    ax.set_xlabel("Fuel Type")
    ax.set_ylabel("Price (cents per liter)")
    ax.set_title("Fuel Prices: Independent vs. Cheapest Franchise Stores")
    ax.set_xticks(x)
    ax.set_xticklabels(merged_df["FuelType"])
    ax.legend()

    ax.set_ylim(bottom=90)
    ax.set_yticks(range(90, 231, 10))
    plt.tight_layout()
    answer8='''Insights:
    From the graph, It is evident that Speedway offers DL,P95 and E85,Costco offers E10 and P98,Metro Fuel offers LPG,Pearl Energy offers PDL 
    and U-Go offers U91 in the cheapest prices for the respective fuel types,which gives us the insights that particular brands are cheaper 
    for particular fuel types than the independent stores.'''
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    plt.savefig(f"{studentid}-Q8.png")
    log("QUESTION 8", other=answer8)
    return answer8


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_9(df7):
    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    def truncate_date(x):
        y=x.split(' ')
        return y[0]
    # Data from NSW Regions Site
    data = {
    'Region': [
        'Sydney', 'Central Coast', 'Newcastle and Lake Macquarie', 'Illawarra',
        'Richmond - Tweed', 'Southern Highlands and Shoalhaven', 'Hunter Valley exc Newcastle',
        'Mid North Coast', 'Coffs Harbour - Grafton', 'Capital Region', 'Central West',
        'Riverina', 'New England and North West', 'Murray', 'Far West and Orana'
    ],
    'Postcode': [
        '2000 2006 2007 2008 2009 2010 2011 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026 2027 2028 2029 2030 2031 2032 2033 2034 2035 2036 2037 2038 2039 2040 2041 2042 2043 2044 2045 2046 2047 2048 2049 2050 2052 2060 2061 2062 2063 2064 2065 2066 2067 2068 2069 2070 2071 2072 2073 2074 2075 2076 2077 2079 2080 2081 2082 2083 2084 2085 2086 2087 2088 2089 2090 2092 2093 2094 2095 2096 2097 2099 2100 2101 2102 2103 2104 2105 2106 2107 2108 2109 2110 2111 2112 2113 2114 2115 2116 2117 2118 2119 2120 2121 2122 2123 2125 2126 2127 2128 2129 2130 2131 2132 2133 2134 2135 2136 2137 2138 2139 2140 2141 2142 2143 2144 2145 2146 2147 2148 2150 2151 2152 2153 2154 2155 2156 2157 2158 2159 2160 2161 2162 2163 2164 2165 2166 2167 2168 2170 2171 2172 2173 2174 2175 2176 2177 2178 2179 2190 2191 2192 2193 2194 2195 2196 2197 2198 2199 2200 2203 2204 2205 2206 2207 2208 2209 2210 2211 2212 2213 2214 2216 2217 2218 2219 2220 2221 2222 2223 2224 2225 2226 2227 2228 2229 2230 2231 2232 2233 2234 2555 2556 2557 2558 2559 2560 2563 2564 2565 2566 2567 2568 2569 2570 2571 2572 2573 2574 2745 2747 2748 2749 2750 2752 2753 2754 2755 2756 2757 2758 2759 2760 2761 2762 2763 2765 2766 2767 2768 2769 2770 2773 2774 2775 2776 2777 2778 2779 2780 2782 2783 2784 2785 2786 2787 2790',
        '2083 2250 2251 2256 2257 2258 2259 2260 2261 2262 2263 2775',
        '2259 2264 2265 2267 2278 2280 2281 2282 2283 2284 2285 2286 2287 2289 2290 2291 2292 2293 2294 2295 2296 2297 2298 2299 2300 2302 2303 2304 2305 2306 2307 2308 2318 2322 2323',
        '2500 2502 2505 2506 2508 2515 2516 2517 2518 2519 2522 2525 2526 2527 2528 2529 2530 2533 2534 2535 2560 2577',
        '2469 2470 2471 2472 2473 2474 2475 2476 2477 2478 2479 2480 2481 2482 2483 2484 2485 2486 2487 2488 2489 2490',
        '2533 2535 2536 2538 2539 2540 2541 2571 2575 2576 2577 2578 2579 2622',
        '2250 2311 2312 2314 2315 2316 2317 2318 2319 2320 2321 2322 2323 2324 2325 2326 2327 2328 2329 2330 2331 2333 2334 2335 2336 2337 2338 2420 2421 2850',
        '2312 2324 2415 2420 2422 2423 2424 2425 2426 2427 2428 2429 2430 2431 2439 2440 2441 2443 2444 2445 2446 2447 2448 2449 2898',
        '2370 2441 2448 2449 2450 2452 2453 2454 2455 2456 2460 2462 2463 2464 2465 2466 2469',
        '2536 2537 2539 2545 2546 2548 2549 2550 2551 2579 2580 2581 2582 2583 2584 2585 2586 2587 2594 2611 2618 2619 2620 2621 2622 2623 2625 2626 2627 2628 2629 2630 2631 2632 2633 2666 2726 2787 2794 2803 2807 2808 2900',
        '2329 2580 2583 2594 2665 2666 2668 2669 2671 2672 2721 2785 2786 2787 2790 2791 2792 2793 2794 2795 2797 2798 2799 2800 2804 2805 2806 2807 2808 2809 2810 2823 2825 2844 2845 2846 2847 2848 2849 2850 2852 2864 2865 2866 2867 2868 2869 2870 2871 2873 2874 2875 2876 2877',
        '2588 2590 2594 2611 2624 2629 2640 2642 2644 2645 2649 2650 2651 2652 2653 2655 2656 2658 2661 2663 2665 2666 2668 2669 2675 2678 2680 2681 2700 2701 2702 2703 2705 2706 2707 2711 2720 2722 2725 2727 2729 2730 3707 3709',
        '2338 2339 2340 2341 2342 2343 2344 2345 2346 2347 2350 2351 2352 2353 2354 2355 2356 2358 2359 2360 2361 2365 2369 2370 2371 2372 2379 2380 2381 2382 2386 2387 2388 2390 2397 2398 2399 2400 2401 2402 2403 2404 2405 2406 2408 2409 2410 2411 2453 2469 2475 2476 2833 4383 4385',
        '2640 2641 2642 2643 2644 2645 2646 2647 2648 2650 2658 2659 2660 2700 2707 2710 2711 2712 2713 2714 2715 2716 2717 2731 2732 2733 2734 2735 2736 2737 2738 2739 2878 3490 3494 3498 3501 3505 3549 3564 3579 3585 3586 3639 3644 3691 3694 3709',
        '2357 2826 2818 2379 2381 2386 2387 2388 2395 2396 2648 2672 2820 2821 2822 2823 2824 2825 2827 2828 2829 2830 2831 2832 2833 2834 2835 2836 2839 2840 2842 2843 2850 2852 2866 2867 2868 2869 2877 2878 2879 2880 4493'
    ]
    }
    # Converting and preprocessing the data
    postcodes_df= pd.DataFrame(data)
    postcodes_df['Postcode'] = postcodes_df['Postcode'].str.split()
    postcodes_df = postcodes_df.explode('Postcode')
    postcodes_df = postcodes_df.drop_duplicates(subset='Postcode', keep='first')
    dtype_map={
        'Postcode': 'int64',
        'Region': 'string',
    }
    postcodes_df=postcodes_df.astype(dtype_map)

    # Updating the regions for df7
    df9 = df7.merge(postcodes_df,on=['Postcode'],how='left')
    df9['PriceUpdatedDate']= df9['PriceUpdatedDate'].apply(truncate_date)

    daily_station_df1=df9.groupby(['Name','FuelType','PriceUpdatedDate']).agg({'Price': 'mean','Postcode': 'first','Region':'first'}).round(2)
    daily_postcode_df1=daily_station_df1.groupby(['Postcode','FuelType','PriceUpdatedDate']).agg({'Price': 'mean','Region':'first'}).round(2)
    avg_postcode_df1=daily_postcode_df1.groupby(['Postcode','FuelType']).agg({'Price': 'mean','Region':'first'}).round(2)
    avg_Region_df1 = avg_postcode_df1.groupby(['Region','FuelType']).agg({'Price': 'mean',}).round(2)
    region_fuelType = pd.MultiIndex.from_product([df9['Region'].unique(), df9['FuelType'].unique()],names=['Region', 'FuelType'])
    avg_Region_df1=avg_Region_df1.reindex(region_fuelType , fill_value=0).reset_index()
    avg_Region_df1=avg_Region_df1.sort_values(by=['Region', 'FuelType'])

    #pivoting table for better visualisation
    pivot_df = avg_Region_df1.pivot(index='Region', columns='FuelType', values='Price')
    pivot_df.drop(['E85'],axis=1,inplace=True)
    pivot_df=pivot_df[['P98', 'U91', 'E10', 'P95', 'PDL', 'DL', 'LPG']]

    x = np.arange(len(pivot_df.index)) * 1.5  
    width = 0.17     

    fig, ax = plt.subplots(figsize=(15, 10))  

    
    for i, fuel_type in enumerate(pivot_df.columns):
        ax.bar(x + i * width, pivot_df[fuel_type], width, label=fuel_type)

    
    ax.set_xlabel('Region', fontsize=12)
    ax.set_ylabel('Fuel Price (cents per litre)', fontsize=12)
    ax.set_title('Fuel Prices by Region and Fuel Type', fontsize=16)
    ax.set_xticks(x + width * (len(pivot_df.columns) - 1) / 2)
    ax.set_xticklabels(pivot_df.index, rotation=45, ha='right', fontsize=10)

    ax.set_ylim(bottom=170)
    ax.set_yticks(range(100, 221, 10))
    ax.legend(title='Fuel Type', bbox_to_anchor=(1, 1), loc='upper left')
    ax.grid(axis='y', alpha=0.3)

    plt.subplots_adjust(bottom=0.2, right=0.85)

    plt.tight_layout()
    answer9='''Assumption: 
                - 2826,2818 in Far West and Orana (Not listed NSW Regions and Postcodes site).
                - I have considered E85 as the least choice among fuels and
                  dropped E85 because E85 was only sold in 3 regions and only few stores sell them in each region.
               Explanation:
                - From the graph, you can see that the ranges of the almost all fuel types except LPG just differ 
                  by 5 to 8 cents per litre.
                - I could see for LPG there is a huge difference in price , which is at lowest in Sydney around 108 cents
                  and the highest being sold at Richmond areas for 140 cents. 
                - Since, most of the fuels are fairly charged among all the regions,I feel that NSW customers in regional areas 
                  are not unfairly charged.'''
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    plt.savefig(f"{studentid}-Q9.png")
    log("QUESTION 9", other=answer9)
    return answer9


######################################################
# NOTE: DO NOT MODIFY THE MAIN FUNCTION BELOW ...
######################################################
if __name__ == "__main__":
    df1 = question_1("fuel.csv")
    df2 = question_2(df1.copy(True))
    df3 = question_3("postcodes.json")
    df4 = question_4(df2.copy(True), df3.copy(True))
    df5 = question_5(df4.copy(True))
    df6 = question_6(df4.copy(True), df5.copy(True))
    df7 = question_7(df6.copy(True))
    answer8 = question_8(df7.copy(True))
    answer9 = question_9(df7.copy(True))
