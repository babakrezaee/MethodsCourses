
import delimited "https://raw.githubusercontent.com/babakrezaee/MethodsCourses/master/LeidenUniv_MAQM2020/Datasets/Corona_WorldData_Daily_Apr15_ecdc.csv", clear


collapse (sum) cases deaths (max) popdata2018, by(countryterritorycode countriesandterritories)

rename countryterritorycode ISOcode

rename countriesandterritories Country

drop if ISOcode==""

gen popdata2018_log=log10(1+popdata2018)
gen cases_log=log10(1+cases)
