---
sort: 3
---

# Using Custom Scripts

Clients can run custom behavior scripts to generate data which fits your specific research need. For example, you may wish to have clients browse various social media sites, or log in and utilize a specific service.

## Python

### Specifying a custom script
Fortunately it's easy to specify arbitrary scripts as client behaviors. Any Python script placed in the directory `scripts/custom/<filename.py>` can be used as a behavior script with the behavior configuration string of `"custom/<filename.py>"`.

### Requiring additional Python packages
Client containers already come with Selenium installed as a pip requirement. If your script requires additional pip packages, you can place them in `scripts/custom/requirements.txt`.

### Starting examples
Since driving web browsing behavior with Selenium is probably a very use case, we've created a few starter Python scripts at [dane-tool/starter-scripts](https://github.com/dane-tool/starter-scripts/) which cover the webdriver setup process and general web interaction. You are more than welcome to copy and modify and build off of these scripts.

## Shell

Not yet implemented.
