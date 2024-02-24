import sys

sys.stdout.write("MAILFROM: <jeffay@cs.unc.edu>\n")
sys.stdout.write("MAIL FROM <jeffay@cs.unc.edu>\n")
sys.stdout.write("RCPT TO : < bob@cs.unc.edu>\n")
sys.stdout.write("MAIL FROM: <jeffay @cs.unc.edu>\n")
sys.stdout.write("MAIL FROM: <jsbrown@unc.edu>\n")
sys.stdout.write("RCPT TO: < bob@cs.unc.edu\n")
sys.stdout.write("MAILFROM: <jeffay @cs.unc.edu>\n")

sys.stdout.write("MAIL FROM: <jsbrown@unc.edu>\n")
sys.stdout.write("DATA \n")

sys.stdout.write("MAIL FROM: <jsbrown@unc.edu>\n")
sys.stdout.write("RCPT TO: <jsbrown@unc.edu>\n")
sys.stdout.write("MAIL FROM: <jsbrown@unc.edu>\n")

sys.stdout.write("RCPT TO: <jsbrown@unc.edu>\n")
