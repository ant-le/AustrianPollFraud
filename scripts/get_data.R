### Austria

url_austria_06 <- "https://en.wikipedia.org/wiki/2006_Austrian_legislative_election#Opinion_polling"

austria_session_06 <- polite::bow(url = url_austria_06, user_agent = "Polling error - philipp.bosch@uni-konstanz.de")

austria_session_06 %>% 
  polite::scrape() -> austria_results_06

austria_results_06 %>% 
  rvest::html_node(xpath = "/html/body/div[3]/div[3]/div[5]/div[1]/table[3]") %>% 
  html_table() %>% 
  .[1:8] %>% 
  rename(institute = 1, date = 2) %>% 
  slice(-1) %>% 
  filter(str_detect(institute, "election", negate = TRUE)) %>% 
  janitor::clean_names() %>% 
  mutate(across(,~ str_remove_all(.x,  pattern = "\\[[\\s\\S]*\\]"))) %>%
  mutate(across(!c(date), type.convert)) %>% 
  mutate(date = str_squish(date)) %>%
  mutate(date = lubridate::dmy(date)) -> austria_polls_06




url_austria_08 <- "https://en.wikipedia.org/wiki/Opinion_polling_for_the_2008_Austrian_legislative_election"

austria_session_08 <- polite::bow(url = url_austria_08, user_agent = "Polling error - philipp.bosch@uni-konstanz.de")

austria_session_08 %>% 
  polite::scrape() -> austria_results_08


austria_results_08 %>% 
  rvest::html_node(xpath = "/html/body/div[3]/div[3]/div[5]/div[1]/table[2]") %>% 
  html_table() %>% 
  rename(institute = 1, date = 2) %>% 
  filter(str_detect(institute, "Election|Results", negate = TRUE)) %>% 
  janitor::clean_names() %>% 
  mutate(across(,~ str_remove_all(.x,  pattern = "\\[[\\s\\S]*\\]"))) %>%
  mutate(across(,~ str_remove_all(.x,  pattern = "\\(|\\)"))) %>% 
  mutate(across(everything(), ~ na_if(.x, "—"))) %>% 
  mutate(across(everything(), ~ na_if(.x, "~"))) %>% 
  mutate(across(everything(), ~ na_if(.x, "#"))) %>% 
  filter(str_detect(fpo, "–", negate = TRUE)) %>% 
  filter(str_detect(bzo, "<|>", negate = TRUE)) %>% 
  mutate(across(!c(date), type.convert)) %>% 
  mutate(date = str_squish(date)) %>%
  mutate(date = lubridate::ymd(date)) -> austria_polls_08



url_austria_13 <- "https://en.wikipedia.org/wiki/2013_Austrian_legislative_election#Opinion_polling"

austria_session_13 <- polite::bow(url = url_austria_13, user_agent = "Polling error - philipp.bosch@uni-konstanz.de")

austria_session_13 %>% 
  polite::scrape() -> austria_results_13

austria_results_13 %>% 
  rvest::html_node(xpath = "/html/body/div[3]/div[3]/div[5]/div[1]/table[3]") %>% 
  html_table() %>% 
  rename(institute = 1, date = 2) %>% 
  janitor::clean_names() %>% 
  mutate(across(everything(), ~ na_if(.x, "-"))) %>%
  mutate(across(everything(), ~ str_remove(.x, "%"))) %>% 
  mutate(across(!c(date), type.convert)) %>%
  mutate(date = str_squish(date)) %>%
  mutate(date = lubridate::ymd(date)) -> austria_polls_13




url_austria_17 <- "https://en.wikipedia.org/wiki/Opinion_polling_for_the_2017_Austrian_legislative_election"

austria_session_17 <- polite::bow(url = url_austria_17, user_agent = "Polling error - philipp.bosch@uni-konstanz.de")

austria_session_17 %>% 
  polite::scrape() -> austria_results_17

austria_results_17 %>% 
  rvest::html_node(xpath = "/html/body/div[3]/div[3]/div[5]/div[1]/table[1]") %>% 
  html_table() %>% 
  rename(institute = 1, date = 2) %>%
  tail(-2) %>% 
  filter(institute != "") %>% 
  select(-Lead) %>% 
  janitor::clean_names() %>% 
  mutate(across(everything(), ~ na_if(.x, "–"))) %>%
  mutate(across(everything(),~ str_remove_all(.x,  pattern = "\\[[\\s\\S]*\\]"))) %>%
  filter(str_detect(fpo, "–", negate = TRUE)) %>% 
  mutate(across(!c(date), type.convert)) %>%
  mutate(date = str_squish(date)) %>%
  mutate(date = lubridate::ymd(date)) -> austria_polls_17


### polls prior to 2017 but after 2013 election



austria_results_17 %>% 
  rvest::html_node(xpath = "/html/body/div[3]/div[3]/div[5]/div[1]/table[2]") %>% 
  html_table() %>% 
  rename(institute = 1, date = 2) %>% 
  filter(str_detect(institute, "election", negate = TRUE)) %>% 
  filter(institute != "") %>% 
  select(-Lead) %>% 
  tail(-1) %>% 
  janitor::clean_names() %>% 
  mutate(across(everything(), ~ na_if(.x, "–"))) %>%
  mutate(across(everything(),~ str_remove_all(.x,  pattern = "\\[[\\s\\S]*\\]"))) %>%
  mutate(across(!c(date), type.convert)) %>%
  mutate(date = str_squish(date)) %>%
  mutate(date = lubridate::ymd(date)) -> austria_polls_14_16


url_austria_19 <- "https://en.wikipedia.org/wiki/Opinion_polling_for_the_2019_Austrian_legislative_election"

austria_session_19 <- polite::bow(url = url_austria_19, user_agent = "Polling error - philipp.bosch@uni-konstanz.de")

austria_session_19 %>% 
  polite::scrape() -> austria_results_19

austria_results_19 %>% 
  rvest::html_node(xpath = "/html/body/div[3]/div[3]/div[5]/div[1]/table[1]") %>% 
  html_table() %>% 
  rename(institute = 1, date = 2) %>%
  filter(str_detect(institute, "election", negate = TRUE)) %>% 
  filter(institute != "") %>% 
  select(-Lead) %>% 
  tail(-1) %>% 
  filter(str_detect(date, "–")) %>% 
  mutate(date = str_extract(date, "(?<=–).*")) %>% 
  janitor::clean_names() %>% 
  mutate(across(everything(), ~ na_if(.x, "?"))) %>%
  mutate(across(!c(date), type.convert)) %>%
  mutate(date = str_squish(date)) %>%
  mutate(date = lubridate::ymd(date)) -> austria_polls_19