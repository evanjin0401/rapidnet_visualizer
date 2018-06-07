
def LookupConfig (map, key):
  if key in map:
    return map[key]
  else:
    return map['Default']
  
  
# ######
# Important Note: All maps should define a value for key 'Default' 
# ######

Config_AnimationSpeed = {
# For slower animation, pick smaller values

'Default': 340, # For LS and HSLS
'DSR': 80,
'Epidemic': 140,
'MAX': 10,
'MIN': 2000,
'STEP': 20,
'Chord': 2000,
}

Config_Application_Folder = '../trunk/src/applications'

Config_Applications = {

1: ('sim-ls-periodic/sim-ls-periodic', 'Link State Periodic'),
2: ('sim-hsls-periodic/sim-hsls-periodic', 'HSLS Periodic'),
3: ('sim-ls-triggered/sim-ls-triggered', 'Link State Triggered'),
4: ('sim-hsls-triggered/sim-hsls-triggered', 'HSLS Triggered'),
5: ('../../../branches/ws_cliu_olsr2/src/applications/olsr2/olsr2', 'OLSR'),
6: ('dsr/dsr', 'DSR'),
7: ('epidemic/epidemic', 'Epidemic'),
8: ('chord/chord', 'Chord'),
}

Config_Bandwidth_Styles = {
1: ('low', 'Low (Bandwidth)'),
2: ('med', 'Medium'),
3: ('high', 'High'),
4: ('veryhigh', 'Very High'),
}

Config_Legends = {

'DSR': {1: ('eQuery', 'Source'), 2: ('eQuery_Dst', 'Destination'), 3: ('ePathDst', 'Query Received'),
        4: ('ePathSrc', 'Reply Sent'), 5: ('tBestPath', 'Received Best Path'),
        100: ('Default', 'Default')
        },
'Epidemic': {1: ('eMessageInjectOriginal', 'Source'), 2: ('eMessageInjectDst', 'Destination'),
             3: ('tMessage', 'Message Received'), 4: ('eMessageEnd', 'Destination Received Message'),
             100: ('Default', 'Default')
             },
'Link State Periodic': Config_Bandwidth_Styles,
'Link State Triggered': Config_Bandwidth_Styles,
'HSLS Periodic': Config_Bandwidth_Styles,
'HSLS Triggered': Config_Bandwidth_Styles,
'OLSR': Config_Bandwidth_Styles,
'Discovery': Config_Bandwidth_Styles,

'Chord': {1: ('chordRing', 'Joined the ring'),
          100: ('Default', 'Default'),
          },
#'Default': {100: ('Default', 'Default'),
#            },
'Default': Config_Bandwidth_Styles,
}

Config_Link_Legends = {

'Epidemic': {1: ('eBitVectorReply', 'Summary Exchange')},
'Default': {},
}
