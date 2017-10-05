from robot.api import TestSuite
from robot.running import TestCase, Keyword

#suite = TestSuite('Activate Skynet')
#suite.resource.imports.library('OperatingSystem')
#test = suite.tests.create('Should Activate Skynet', tags=['smoke'])
#test.keywords.create('Set Environment Variable', args=['SKYNET', 'activated'], type='setup')
#test.keywords.create('Environment Variable Should Be Set', args=['SKYNET'])

suite = TestSuite('suite 1')
print('0 !!!!')
suite.tests
print('1 !!!!')
tc1 = suite.tests.create('TC 1', tags=['rat'])
print(suite.tests)
print(suite.tests.append)
print('2 !!!!')
suite.tests.append(tc1)
print('3 !!!!')
tc2 = TestCase('TC 2', tags=['mat'], template='log to console')
suite.tests.append(tc2)
print('tc2', tc2.keywords)
tc2.keywords.append(Keyword('log to console', args=['B____B']))
print('4 !!!!')
tc1.keywords.create('log to console', args=['A_____A'])

result = suite.run(output=None, critical='rat')
result = suite.run(output='/tmp/output.xml', critical='rat')
#result = suite.run(output='/tmp/skynet.xml', critical='rat')
#
#assert result.return_code == 0
#assert result.suite.name == 'suite 1'
#test = result.suite.tests[0]
#assert test.name == 'TC 1'
#assert test.passed and test.critical
#stats = result.suite.statistics
#assert stats.critical.total == 1 and stats.critical.failed == 0
#
#
from robot.api import ResultWriter
ResultWriter(result).write_results(report=None, log='/tmp/log.html')
ResultWriter('/tmp/output.xml').write_results(report=None, log='/tmp/log.html')

# Report and xUnit files can be generated based on the result object.
#ResultWriter(result).write_results(report='/tmp/skynet.html', log=None)
# Generating log files requires processing the earlier generated output XML.
#ResultWriter('/tmp/skynet.xml').write_results()
