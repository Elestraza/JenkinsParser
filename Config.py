import xml.etree.ElementTree as ET

class Config:
    @staticmethod
    def createConfig(jk, configNew=True, jobName="", parameters=None, description="Base description"): # Универсальная функция создания/изменения конфига. Применяется в updateConfig и createdJob
        # Параметры задаются в стиле
        # createJob("testAPI", parameters = {
        #     'bool_param': {'type': 'Boolean', 'description': 'Boolean параметр', 'defaultValue': 'true'},
        #     'string_param': {'type': 'String', 'description': 'String параметр', 'defaultValue': 'default_value'}
        # }, description="Test case")
        config = ''
        if configNew is False:
            job = jk.get_job(jobName)
            config = job.get_config()
            
        elif configNew:
            xmlStart = f'''<?xml version='1.1' encoding='UTF-8'?>
                <project>
                    <actions/>
                    <description>{description}</description>
                    <keepDependencies>false</keepDependencies>
                    <properties>
                        <hudson.model.ParametersDefinitionProperty>
                            <parameterDefinitions>'''
            xmlEnd = f'''
                            </parameterDefinitions>
                        </hudson.model.ParametersDefinitionProperty>
                    </properties>
                </project>
            '''
            config = xmlStart + xmlEnd
        if parameters != None:
            root = ET.fromstring(config)
            parameter_definitions = root.find(".//parameterDefinitions")
            for paramName, paramData in parameters.items():
                paramType = paramData.get('type')
                paramDesc = paramData.get("description", "")
                paramDefault = paramData.get("defaultValue", "")
                if paramType == "GitHub":
                    paramXml = f'''
                        <com.coravy.hudson.plugins.github.GithubProjectProperty plugin="github@1.38.0">
                            <projectUrl>{paramDefault}</projectUrl>
                            <displayName>{paramName}</displayName>
                        </com.coravy.hudson.plugins.github.GithubProjectProperty>
                    '''
                if paramType == "Boolean":
                    paramXml = f'''
                        <hudson.model.BooleanParameterDefinition>
                            <name>{paramName}</name>
                            <description>{paramDesc}</description>
                            <defaultValue>{paramDefault}</defaultValue>
                        </hudson.model.BooleanParameterDefinition>
                    '''
                elif paramType == "String":
                    paramXml = f'''
                        <hudson.model.StringParameterDefinition>
                            <name>{paramName}</name>
                            <description>{paramDesc}</description>
                            <defaultValue>{paramDefault}</defaultValue>
                        </hudson.model.StringParameterDefinition>
                    '''
                elif paramType == "Choice":
                    choices = paramData.get("choices", [])  # Список возможных вариантов выбора
                    paramXml = f'''
                        <hudson.model.ChoiceParameterDefinition>
                            <name>{paramName}</name>
                            <description>{paramDesc}</description>
                            <choices class="java.util.Arrays$ArrayList">
                                <a class="string-array">
                                    {"".join(f'<string>{choice}</string>' for choice in choices)}
                                </a>
                            </choices>
                            <defaultValue>{paramDefault}</defaultValue>
                        </hudson.model.ChoiceParameterDefinition>
                    '''
                elif paramType == "Credentials":
                    credentials_id = paramData["credentialsId", ""]  # Идентификатор учетных данных
                    paramXml = f'''
                        <com.cloudbees.plugins.credentials.common.IdCredentialsParameter>
                            <name>{paramName}</name>
                            <description>{paramDesc}</description>
                            <defaultValue>{paramDefault}</defaultValue>
                            <credentialsId>{credentials_id}</credentialsId>
                        </com.cloudbees.plugins.credentials.common.IdCredentialsParameter>
                    '''
                elif paramType == "File":
                    fileLocation = paramData['location']  # Местоположение файла
                    paramXml = f'''
                        <hudson.model.FileParameterDefinition>
                            <name>{paramName}</name>
                            <description>{paramDesc}</description>
                            <file>{fileLocation}</file>
                            <defaultValue>{paramDefault}</defaultValue>
                        </hudson.model.FileParameterDefinition>
                    '''
                elif paramType == "MultiLineString":
                    paramXml = f'''
                        <hudson.model.TextParameterDefinition>
                            <name>{paramName}</name>
                            <description>{paramDesc}</description>
                            <defaultValue>{paramDefault}</defaultValue>
                        </hudson.model.TextParameterDefinition>
                    '''
                elif paramType == "Run":
                    paramXml = f'''
                        <hudson.model.RunParameterDefinition>
                            <name>{paramName}</name>
                            <description>{paramDesc}</description>
                            <projectName>{paramDefault}</projectName>
                        </hudson.model.RunParameterDefinition>
                    '''
                    
                else :
                    paramXml = f''''''
                ET.SubElement(parameter_definitions, 'param').text = paramXml
            config = ET.tostring(root, encoding='UTF-8')
            print(config)
        return config