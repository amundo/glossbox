import re
import sys
import json
import codecs
from toolbox2json import toolbox2json
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def process(iu): 
  if iu['ELANParticipant'] != '\ ':
    iu['ELANParticipant'] = iu['ELANParticipant'].upper() + ';'
  #iu['ds'] = iu['ds'].replace('@', '{{@}}')
  iu['mb'] = iu['mb'].replace('- ', '-').replace(' -', '-').replace(' =', '=').replace('= ', '=')
  iu['ge'] = iu['ge'].replace('- ', '-').replace(' -', '-').replace(' =', '=').replace('= ', '=')
  #iu['gn'] = iu['gn'].replace('- ', '-').replace(' -', '-').replace(' =', '=').replace('= ', '=')
  iu['ge'] = small_capify(iu['ge'])
  return iu

# def trailing_citation(iu):
#   citation = [ius[0]]
#   begin_time = ius[0]['ELANBegin']
#   end_time = ius[-1]['ELANEnd']
#   first_ref = ius[0]['ref']
#   for iu in ius:
#     if iu['ref'] != first_ref:
#       iu['ref'] = ''
#     else:
#       iu['ref'] = iu['ref'] + ', '

def remove_repeated_users(ius):
  new_ius = [ius[0]]
  current = ius[0]['ELANParticipant']
  for iu in ius[1:]:
    if iu['ELANParticipant'] == current:
      iu['ELANParticipant'] = '\ '
    else:
      current = iu['ELANParticipant']
    new_ius.append(iu)
  return new_ius

def small_capify(gloss):
  def lower_replace(match):
     return '\\textsc{' + match.group(1).lower() + '}' 

  substituted = re.sub(r'([A-Z][A-Z]+)', lower_replace, gloss) 
  return substituted 

def boundary_times(ius):
  first_iu = ius[0]
  last_iu = ius[-1]

  first_iu_begin = first_iu['ELANBegin']
  last_iu_end = last_iu['ELANEnd']

  return { 
     'first_iu_begin' : first_iu_begin,
     'last_iu_end' : last_iu_end
  }

def filter_ius(ius):
  ius = remove_repeated_users(ius)
  ius_boundary_times = boundary_times(ius)

  ius_with_boundaries = []
  
  for iu in ius: 
    iu.update(ius_boundary_times)
    ius_with_boundaries.append(iu)

  return ius_with_boundaries
  
def render_template(iu, template_path): 
  template = open(template_path).read().decode('utf-8')
  iu = process(iu)
  return template.format(**iu)

def toSeconds(HMSm):
    HMSm = HMSm.replace('.', ' ').replace(':', ' ').split(' ')
    H, M, S, m = HMSm
    return float(H) * 3600 + float(M) * 60 + float(S) + float(m) / 1000.0

def render_ius(line):  
  tokens = line.strip().split()
  tokens.pop(0)
  begin = float(toSeconds(tokens[1]))
  end = float(toSeconds(tokens[2]))
  result = line

  matched_ius = [iu for iu in ius if iu['ELANBegin'] >= begin and iu['ELANEnd'] <= end]

  last = matched_ius[-1]
  nonlast_ius = matched_ius[:-1]

  for iu in nonlast_ius:
       result += render_template(iu, 'templates/example.latex') 
  result += render_template(last, 'templates/last_example.latex') 
  print result

  return result

if __name__ == "__main__":
  import sys

  if len(sys.argv) != 3: 
    print 'Usage: python glossbox.py  <toolbox file> <glossbox file>'
    exit()
  
  toolbox_file = sys.argv[1]
  glossbox_file = sys.argv[2]
  print glossbox_file 
  print toolbox_file 

  ius = toolbox2json(open(toolbox_file).read().decode('utf-8'))

  for line in open(glossbox_file):
    if line.strip().startswith('%%  GLOSSBOX'):
      print render_ius(line),
    else:
      print line,
