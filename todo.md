#### todos
- [ ] company names currently need to be seperated by the specific seperator "," instead of just an empy seperator " "
- [ ] handle cloudflare etc restrictions
- [x] move stuff to scrapy folder structure
- [ ] validate regex
- [ ] all value information is behind unstructured text
- [ ] allow both company and tag search: implement with 2 different params
- [ ] running the spiders sequentially
- [ ] scrapy itself doesn't work with its configuration, only call modules from script
- [ ] general webdriver initialisation
- [ ] optimizie mappings parsing
- [ ] indeed doesnt seem to filter if not in passed companies list

#### problems
- regular jobsearch params don't transfer from url BUT it does in company search -> change to company intern search !!! funktioniert doch: keine action
DONE
- recheck if filters are selected on search result, since stepstone otherwise returns without them selected sometimes
- 409 error 
MAYBE? using 1 concurrent requests now
- sometimes request just doesn't apply filters? feels random also in regular use



NO NEED FOR SELENIUM! -> indeed contains elements, just show = false