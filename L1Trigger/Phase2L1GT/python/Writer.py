import jinja2
import L1Trigger.Phase2L1GT.Conditions
def conditionwriter(obj):
    templateLoader = jinja2.FileSystemLoader(searchpath="../python/")    # this has to be changed there seems to be a version of this thats called packageloader instead of filesystemloader
    templateEnv = jinja2.Environment(loader=templateLoader,trim_blocks=True,lstrip_blocks=True)
    template = templateEnv.get_template(obj.Template,)
    if(obj.Label == 'L1GTDoubleObjectCond'):
        outputText = template.render(condition_name = obj.Name, dict_item = obj.Cuts,objects_first = obj.InputObjects.get('col1Tag'),objects_second = obj.InputObjects.get('col2Tag'),algo_bit_name = obj.Name) 
    elif(obj.Label == 'L1GTSingleObjectCond'):
        outputText = template.render(condition_name = obj.Name, dict_item = obj.Cuts,object = obj.InputObjects.get('colTag'),algo_bit_name = obj.Name) 
    return outputText

def algounitWriter(obj,conditions):
    templateLoader = jinja2.FileSystemLoader(searchpath="../python/")    # this has to be changed there seems to be a version of this thats called packageloader instead of filesystemloader
    templateEnv = jinja2.Environment(loader=templateLoader,trim_blocks=True,lstrip_blocks=True)
    template = templateEnv.get_template("algounit.template",)
    outputText = template.render(algobits = obj.Assignment, Conditions = conditions)
    return outputText

def writeAlgounitToFile(filename,contents):
    f = open(filename,"w")
    f.write(contents)
    f.close()

    