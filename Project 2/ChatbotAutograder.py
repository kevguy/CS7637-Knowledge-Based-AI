"""
Chatbot Autograder - Updated 11/23/2017.

Please use this file to test your Chatbot class.
https://www.python.org/dev/peps/pep-0008/
function_names and variable:
lowercase with words separated by underscores as necessary to improve readability.
Class names should normally use the CapWords convention (yea!).
"Private" variables start with _
Spaces are the preferred indentation method.
80 characters per line - Is this the 1980's?
I have not used a line printer since college

q/a dictionary structure
type: 
    faq = reworded question from faq
    ood = out of domain question
    new = (P3 only) previous ood question that has been updated with replace
questions: list of questions
    question[0] is asked in pass 1, question[1] is asked in pass 2 (P3 only)
response: expected response from agent
replace: new response sent to agent (P3 only)
         the agent should reply with this response the next time question is asked

"""


import sys, getopt, json, traceback
import Chatbot
from contextlib import redirect_stdout


class Grader:
    def __init__(self):
        self._stats = {'faq': {'count': 0, 'true': 0, 'false': 0, 'idk': 0},
                       'ood': {'count': 0, 'true': 0, 'false': 0, 'idk': 0},
                       'new': {'count': 0, 'true': 0, 'false': 0, 'idk': 0},
                       '2nd': {'count': 0, 'true': 0, 'false': 0, 'idk': 0}}

    def grade(self, agent_response, test_question_type, test_response):
        if test_question_type not in self._stats:
            raise ValueError('Invalid Type in script')

        agent_feedback = False
        self._stats[test_question_type]['count'] += 1
        clean_agent_response = agent_response.split('\n')[0]

        if clean_agent_response == "I do not know.":
            self._stats[test_question_type]['idk'] += 1

        if clean_agent_response == test_response.split('\n')[0]:
            self._stats[test_question_type]['true'] += 1
            agent_feedback = True
        else:
            self._stats[test_question_type]['false'] += 1
            agent_feedback = False
        return agent_feedback

    def header_string(self, feedback):
        retval = "faq_count,faq_true,faq_false,faq_idk,ood_count,ood_true,ood_false,ood_idk"
        if feedback: retval += ",new_count,new_true,new_false,new_idk,2nd_count,2nd_true,2nd_false,2nd_idk"
        return retval

    def result_string(self, feedback):
        result = str(self._stats['faq']['count']) + ','
        result += str(self._stats['faq']['true']) + ','
        result += str(self._stats['faq']['false']) + ','
        result += str(self._stats['faq']['idk']) + ','
        result += str(self._stats['ood']['count']) + ','
        result += str(self._stats['ood']['true']) + ','
        result += str(self._stats['ood']['false']) + ','
        result += str(self._stats['ood']['idk'])
        if feedback:
            result += ','
            result += str(self._stats['new']['count']) + ','
            result += str(self._stats['new']['true']) + ','
            result += str(self._stats['new']['false']) + ','
            result += str(self._stats['new']['idk']) + ','
            result += str(self._stats['2nd']['count']) + ','
            result += str(self._stats['2nd']['true']) + ','
            result += str(self._stats['2nd']['false']) + ','
            result += str(self._stats['2nd']['idk'])

        return result


class Logger:
    def __init__(self, autograder_test_script):
        self._logging = False

        if 'log' in autograder_test_script:
            print("Loggin to file: " + autograder_test_script['log'] + ".log")
            self._log_file = open(autograder_test_script['log'] + ".log", "w")
            self._logging = True

    def logformat(self, replace, _type, question, agent_response, test_response, result):
        retval = ("\nQuestion Type: " + _type)
        retval += ("\nTest Question: " + question)
        retval += ("\nAgent Response: " + agent_response)
        retval += ("\nTest Response: " + test_response)
        if replace:
             retval += ("\nTest Replace: " + replace)
        retval += ("\nResult: " + result)
        retval += '\n'
        return retval

    def logmsg(self, msg):
        if self._logging:
            self._log_file.write(msg)

    def logclose(self):
        if self._logging:
            self._log_file.close()


def ChatbotAutograder(script_filename, verbose):
    print(__doc__.split('.')[0])

    print("Opening script: " + script_filename)
    try:
        with open(script_filename, encoding='utf-8') as json_data:
            autograder_test_script = json.load(json_data)
    except Exception as e:
        print("Failure opening or reading script: " + str(e))
        return 1

    if 'version' in autograder_test_script:
        print("Script version: " + autograder_test_script['version'])
    else:
        print("Version not identified")
        return 1

    if 'script' not in autograder_test_script:
        print("Test script not identified")
        return 1

    if 'faq' not in autograder_test_script:
        print("FAQ filename not identified")
        return 1

    try:
        logit = Logger(autograder_test_script)
    except:
        print("Failed to open log file")
        return 1

    print("Redirecting to file: " + autograder_test_script['log'] + ".out")
    try:
        redirect = open(autograder_test_script['log'] + ".out", "w")
    except:
        print("Failed to open redirection file")
        return 1

    feedback = False
    if autograder_test_script['feedback'] == 'on':
        feedback = True

    regrade_list_of_dicts = []
    print("Opening FAQ: " + autograder_test_script['faq'])
    print("Instantiating Chatbot")
    try:
        chatbot = Chatbot.Chatbot(autograder_test_script['faq'])
    except FileNotFoundError:
        print("Could not find FAQ.")
        return 1

    try:
        grader = Grader()
        print("Running script")
        for qa_dict in autograder_test_script['script']:
            question = qa_dict['questions'][0]
            with redirect_stdout(redirect):
                agent_response = chatbot.input_output(question).split('\n')[0]

            try:
                feedback_to_agent = grader.grade(agent_response, qa_dict['type'], qa_dict['response'])
            except ValueError as e:
                print("Grader Error: {0}".format(e))
                logit.logmsg("Grader Error: {0}".format(e))
                raise

            if not verbose:
                if feedback_to_agent:
                    print('+',end='')
                else:
                    print('-',end='')

            if len(qa_dict['questions'])>1 and feedback and not feedback_to_agent:
                qa_dict_copy = qa_dict.copy()
                qa_dict_copy['type'] = '2nd'
                regrade_list_of_dicts.append(qa_dict_copy)
                if verbose: print("Added to re-ask")

            if 'replace' in qa_dict:
                replace = qa_dict['replace']
            else:
                replace = ""

            if feedback:
                with redirect_stdout(redirect):
                    chatbot.user_feedback(feedback_to_agent, replace)

            logmsg = logit.logformat(replace, qa_dict['type'],
                                     question,
                                     agent_response, qa_dict['response'],
                                     grader.result_string(feedback))
            logit.logmsg(logmsg)
            if verbose: print(logmsg)

        if not verbose: print('|', end='')
        # Ask questions in regrade_list_of_dicts again
        for qa_dict in regrade_list_of_dicts:
            question = qa_dict['questions'][1]
            with redirect_stdout(redirect):
                agent_response = chatbot.input_output(question).split('\n')[0]

            try:
                feedback_to_agent = grader.grade(agent_response, qa_dict['type'], qa_dict['response'])
            except ValueError as e:
                print("Grader Error: {0}".format(e))
                raise

            if not verbose:
                if feedback_to_agent:
                    print('+',end='')
                else:
                    print('-',end='')

            logmsg = logit.logformat("", qa_dict['type'],
                                     question,
                                     agent_response, qa_dict['response'],
                                     grader.result_string(feedback))
            logit.logmsg(logmsg)
            if verbose: print(logmsg)

        logit.logmsg("\n\n\nScript version: " + autograder_test_script['version'])
        logit.logmsg("\nFAQ: " + autograder_test_script['faq'])
        if feedback:
            logit.logmsg("\nFeedback: ON")
        logit.logmsg("\n"+grader.header_string(feedback))
        logit.logmsg("\nResult: " + grader.result_string(feedback))

        print("\n\nResults")
        print(grader.header_string(feedback))
        print(grader.result_string(feedback))

    except Exception as e:
        logit.logmsg("Error during grading: " + str(e))
        print("Error during grading: " + str(e))
        print(traceback.print_exc(file=sys.stdout))
    finally:
        logit.logclose()
        return 1


def main(argv):
    # https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    script_filename = ''
    verbose = False
    try:
        opts, args = getopt.getopt(argv, "hvs:", ["script="])
    except getopt.GetoptError:
        print("Usage: chatbotAutograder.py -s script")
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print("Usage: chatbotAutograder.py -s script")
            sys.exit()
        elif opt in ("-v"):
            verbose = True
        elif opt in ("-s", "--script"):
            script_filename = arg

    if not script_filename:
        print("Usage: chatbotAutograder.py -s script")
        sys.exit(3)

    return ChatbotAutograder(script_filename, verbose)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
