#!/usr/bin/env python

from rdflib import Graph, Namespace, URIRef, Literal
import rdflib
import json

"""
Point count:
- actuators & sensors in schematics:
  23+20+20+20+18+18+18+12+12+18+18+15+12+15+12+15+6+15+12+14+18+18+18+18+18+12+6+12+11+6+18+22+15+10+6+10+9+9=549
- setpoints and other atrificials (11-12 per rool):
  12*60=720
- all in all
  549+720=1269

TODO:
- add media relations
- find a better name for IJ_Valve_Functional_Block
- define Celcius_Temperature_Sensor
- add zone literal?
"""

################################################################################
############################################################## front matter ####
################################################################################

RDF        = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS       = Namespace('http://www.w3.org/2000/01/rdf-schema#')
BRICK      = Namespace('https://brickschema.org/schema/1.0.1/Brick#')
BRICKFRAME = Namespace('https://brickschema.org/schema/1.0.1/BrickFrame#')
BRICKTAG   = Namespace('https://brickschema.org/schema/1.0.1/BrickTag#')

g = Graph()
brickpath = lambda filename: '../../../Brick/'+filename
g.parse(brickpath('Brick.ttl'), format='turtle')
g.parse(brickpath('BrickFrame.ttl'), format='turtle')
g.parse(brickpath('BrickTag.ttl'), format='turtle')
g.bind('rdf'  , RDF)
g.bind('rdfs' , RDFS)
g.bind('brick', BRICK)
g.bind('bf'   , BRICKFRAME)
g.bind('btag' , BRICKTAG)

# building
GTC = Namespace('https://brickschema.org/schema/1.0.1/building_example#')
g.bind('gtc', GTC)

################################################################################
################################################################ constructs ####
################################################################################

def gen_extensions():
    Heat_Power_Meter_Functional_Block = GTC['Heat_Power_Meter_Functional_Block']
    g.add( (Heat_Power_Meter_Functional_Block, RDF.isSubClassOf, BRICK['Functional_Block']) )
    
    Heat_Transfer_Box_Functional_Block = GTC['Heat_Transfer_Box_Functional_Block']
    g.add( (Heat_Transfer_Box_Functional_Block, RDF.isSubClassOf, BRICK['Functional_Block']) )
    
    GTC_VAV_Functional_Block = GTC['GTC_VAV_Functional_Block']
    g.add( (GTC_VAV_Functional_Block, RDF.isSubClassOf, BRICK['Functional_Block']) )
    g.add( (GTC_VAV_Functional_Block, RDFS.subClassOf, BRICK['VAV']) )
    
    IJ_Valve_Functional_Block = GTC['IJ_Valve_Functional_Block']
    g.add( (IJ_Valve_Functional_Block, RDF.isSubClassOf, BRICK['Functional_Block']) )
    
    GTC_Filter_Element_Functional_Block = GTC['GTC_Filter_Element_Functional_Block']
    g.add( (GTC_Filter_Element_Functional_Block, RDF.isSubClassOf, BRICK['Functional_Block']) )
    
    DPT_Functional_Block = GTC['DPT_Functional_Block']
    g.add( (DPT_Functional_Block, RDF.isSubClassOf, BRICK['Functional_Block']) )
    
    GTC_Room_Functional_Block = GTC['GTC_Room_Functional_Block']
    g.add( (GTC_Room_Functional_Block, RDF.isSubClassOf, BRICK['Functional_Block']) )
    
    Celcius_Room_Temperature_Sensor = GTC['Celcius_Temperature_Sensor']
    g.add( (Celcius_Room_Temperature_Sensor, RDFS.subClassOf, BRICK['Sensor']) )
    g.add( (Celcius_Room_Temperature_Sensor, BRICKFRAME.hasTag, BRICKTAG['Room']) )
    g.add( (Celcius_Room_Temperature_Sensor, BRICKFRAME.hasTag, BRICKTAG['Temperature']) )
    g.add( (Celcius_Room_Temperature_Sensor, BRICKFRAME.hasUnit, BRICKTAG['Celcius']) )
    
    Celcius_Room_Temperature_Setpoint = GTC['Celcius_Room_Temperature_Setpoint']
    g.add( (Celcius_Room_Temperature_Setpoint, RDFS.subClassOf, BRICK['Setpoint']) )
    g.add( (Celcius_Room_Temperature_Setpoint, BRICKFRAME.hasTag, BRICKTAG['Room']) )
    g.add( (Celcius_Room_Temperature_Setpoint, BRICKFRAME.hasTag, BRICKTAG['Temperature']) )
    g.add( (Celcius_Room_Temperature_Setpoint, BRICKFRAME.hasUnit, BRICKTAG['Celcius']) )
    
    LEDGO_Lighting_System = GTC['LEDGO_Lighting_System']
    g.add( (LEDGO_Lighting_System, RDFS.subClassOf, BRICK['Lighting_System']) )
    

def gen_electrical (prefix, floors):
    meter        = GTC[prefix+'/main_meter']
    common_meter = GTC[prefix+'/main_common_meter']
    fuse         = GTC[prefix+'/main_fuse']
    common_fuse  = GTC[prefix+'/main_common_fuse']
    submeter_labels = [
        '-A1.0.1',
        '-A1.0.2',
        '-A1.1.1',
        '-A1.1.2',
        '-A1.1.3',
        '-A1.1.4',
        '-A1.2.1',
        '-A1.2.2',
        '-A1.2.3',
        '-A1.2.4',
    ]
    submeters = map(lambda label: GTC[prefix+'/submeter['+label+']'], submeter_labels)
    
    # labels
    g.add( (meter       , RDFS.label, Literal('aggregate of renters charges')) )
    g.add( (common_meter, RDFS.label, Literal('shared charging')) )
    g.add( (fuse        , RDFS.label, Literal('100A')) )
    g.add( (common_fuse , RDFS.label, Literal('250A')) )
    for index in range(len(submeter_labels)):
        g.add( (submeters[index], RDFS.label, Literal(submeter_labels[index])) )
    
    # types
#    g.add( (meter       , RDF.type,   GTC['Electrical_Energy_Meter']) )
#    g.add( (common_meter, RDF.type,   GTC['Electrical_Energy_Meter']) )
    g.add( (meter       , RDF.type, BRICK['Power_Meter']) )
    g.add( (common_meter, RDF.type, BRICK['Power_Meter']) )
    g.add( (meter       , RDF.type,   GTC['Fuse']) )
    g.add( (common_meter, RDF.type,   GTC['Fuse']) )
    for submeter in submeters:
        g.add( (submeter, RDF.type, GTC['Electrical_Energy_Meter']) )
    
    # isPartOf
    for index in range(len(submeter_labels)):
        floor = floors[int(submeter_labels[index].split('.')[1])]
        g.add( (submeters[index], BRICKFRAME['isPartOf'], floor) )
    
    # feeds
    g.add( (fuse       , BRICKFRAME['feeds'], meter) )
    g.add( (common_fuse, BRICKFRAME['feeds'], common_meter) )
    for submeter in submeters:
        g.add( (meter, BRICKFRAME['feeds'], submeter) )
    
    # build hash
    metermap = {}
    for index in range(len(submeter_labels)):
        metermap[submeter_labels[index]] = submeters[index]
    metermap['-A1'] = common_meter
    
    ports = {
        'metermap': metermap,
    }
    return ports

# instantiate a heat exchanger
def gen_hx (prefix):
    fb = GTC[prefix+'/fb']
    pi = GTC[prefix+'/port[pi]']
    po = GTC[prefix+'/port[po]']
    si = GTC[prefix+'/port[si]']
    so = GTC[prefix+'/port[so]']
    
    # types
    g.add( (fb, RDF.type, BRICK['Heat_Exchanger_Functional_Block']) )
    g.add( (pi, RDF.type, BRICK['Heat_Exchanger_Primary_Input']) )
    g.add( (po, RDF.type, BRICK['Heat_Exchanger_Primary_Output']) )
    g.add( (si, RDF.type, BRICK['Heat_Exchanger_Secondary_Input']) )
    g.add( (so, RDF.type, BRICK['Heat_Exchanger_Secondary_Output']) )
    
    # isPartOf
    g.add( (pi, BRICKFRAME['isPartOf'], fb) )
    g.add( (po, BRICKFRAME['isPartOf'], fb) )
    g.add( (si, BRICKFRAME['isPartOf'], fb) )
    g.add( (so, BRICKFRAME['isPartOf'], fb) )
    
    ports = {
        'fb': fb,
        'pi': pi,
        'po': po,
        'si': si,
        'so': so,
    }
    return ports

# instantiate a heating power meter (measures power based on flow and temperature drop)
def gen_heating_power_meter (prefix):
    fb          = GTC[prefix+'/fb']
    s           = GTC[prefix+'/port[supply]']
    r           = GTC[prefix+'/port[return]']
    ms          = GTC[prefix+'/port[metered_supply]']
    mr          = GTC[prefix+'/port[metered_return]']
    flow        = GTC[prefix+'/flow']
    supply_temp = GTC[prefix+'/supply_temp']
    return_temp = GTC[prefix+'/return_temp']
    power       = GTC[prefix+'/power']
    
    # types
    g.add( (fb         , RDF.type,   GTC['Heat_Power_Meter_Functional_Block']) )
    g.add( (s          , RDF.type,   GTC['Heat_Power_Meter_Supply']) )
    g.add( (r          , RDF.type,   GTC['Heat_Power_Meter_Return']) )
    g.add( (ms         , RDF.type,   GTC['Heat_Power_Meter_Metered_Supply']) )
    g.add( (mr         , RDF.type,   GTC['Heat_Power_Meter_Metered_Return']) )
    g.add( (flow       , RDF.type, BRICK['Flow_Sensor']) )
    g.add( (supply_temp, RDF.type,   GTC['Celcius_Temperature_Sensor']) )
    g.add( (return_temp, RDF.type,   GTC['Celcius_Temperature_Sensor']) )
    g.add( (power      , RDF.type,   GTC['Heating_Power_Calculation']) )
    
    # isPartOf
    g.add( (s          , BRICKFRAME['isPartOf'], fb) )
    g.add( (r          , BRICKFRAME['isPartOf'], fb) )
    g.add( (ms         , BRICKFRAME['isPartOf'], fb) )
    g.add( (mr         , BRICKFRAME['isPartOf'], fb) )
    g.add( (flow       , BRICKFRAME['isPartOf'], fb) )
    g.add( (supply_temp, BRICKFRAME['isPartOf'], fb) )
    g.add( (return_temp, BRICKFRAME['isPartOf'], fb) )
    g.add( (power      , BRICKFRAME['isPartOf'], fb) )
    
    # feeds
    g.add( (s          , BRICKFRAME['feeds'], flow) )
    g.add( (flow       , BRICKFRAME['feeds'], supply_temp) )
    g.add( (supply_temp, BRICKFRAME['feeds'], mr) )
    g.add( (mr         , BRICKFRAME['feeds'], return_temp) )
    g.add( (return_temp, BRICKFRAME['feeds'], r) )
    
    # controls
    g.add( (flow       , BRICKFRAME['controls'], power) )
    g.add( (supply_temp, BRICKFRAME['controls'], power) )
    g.add( (return_temp, BRICKFRAME['controls'], power) )
    
    # hasPoint
    g.add( (fb, BRICKFRAME['hasPoint'], flow) )
    g.add( (fb, BRICKFRAME['hasPoint'], supply_temp) )
    g.add( (fb, BRICKFRAME['hasPoint'], return_temp) )
    g.add( (fb, BRICKFRAME['hasPoint'], power) )
    
    ports = {
        'fb': fb,
        'supply': s,
        'return': r,
        'metered_supply': ms,
        'metered_return': mr,
    }
    return ports

# instantiation of a grouping of a heating power meter, heat exchanger, pump and two temperature sensors
def gen_heat_transfer_box (prefix):
    fb          = GTC[prefix+'/fb']
    pi          = GTC[prefix+'/port[pi]']
    po          = GTC[prefix+'/port[po]']
    si          = GTC[prefix+'/port[si]']
    so          = GTC[prefix+'/port[so]']
    hpm         = gen_heating_power_meter(prefix+'/hpm')
    hx          = gen_hx(prefix+'/hx')
    pump        = GTC[prefix+'/pump']
    supply_temp = GTC[prefix+'/supply_temp']
    return_temp = GTC[prefix+'/return_temp']
    
    # types
    g.add( (fb         , RDF.type,   GTC['Heat_Transfer_Box_Functional_Block']) )
    g.add( (pi         , RDF.type,   GTC['Heat_Transfer_Box_Primary_Input']) )
    g.add( (po         , RDF.type,   GTC['Heat_Transfer_Box_Primary_Output']) )
    g.add( (si         , RDF.type,   GTC['Heat_Transfer_Box_Secondary_Input']) )
    g.add( (so         , RDF.type,   GTC['Heat_Transfer_Box_Secondary_Output']) )
    g.add( (pump       , RDF.type, BRICK['Pump']) )
    g.add( (supply_temp, RDF.type,   GTC['Celcius_Temperature_Sensor']) )
    g.add( (return_temp, RDF.type,   GTC['Celcius_Temperature_Sensor']) )
    
    # isPartOf
    g.add( (pi         , BRICKFRAME['isPartOf'], fb) )
    g.add( (po         , BRICKFRAME['isPartOf'], fb) )
    g.add( (si         , BRICKFRAME['isPartOf'], fb) )
    g.add( (so         , BRICKFRAME['isPartOf'], fb) )
    g.add( (hpm['fb']  , BRICKFRAME['isPartOf'], fb) )
    g.add( (hx['fb']   , BRICKFRAME['isPartOf'], fb) )
    g.add( (pump       , BRICKFRAME['isPartOf'], fb) )
    g.add( (supply_temp, BRICKFRAME['isPartOf'], fb) )
    g.add( (return_temp, BRICKFRAME['isPartOf'], fb) )
    
    # feeds
    g.add( (pi                   , BRICKFRAME['feeds'], hpm['supply']) )
    g.add( (hpm['metered_supply'], BRICKFRAME['feeds'], hx['pi']) )
    g.add( (hx['po']             , BRICKFRAME['feeds'], hpm['metered_return']) )
    g.add( (hpm['return']        , BRICKFRAME['feeds'], po) )
    g.add( (so                   , BRICKFRAME['feeds'], return_temp) )
    g.add( (return_temp          , BRICKFRAME['feeds'], hx['si']) )
    g.add( (hx['so']             , BRICKFRAME['feeds'], pump) )
    g.add( (pump                 , BRICKFRAME['feeds'], supply_temp) )
    g.add( (supply_temp          , BRICKFRAME['feeds'], so) )
    
    # hasPoint
    g.add( (fb, BRICKFRAME['hasPoint'], hpm['fb']) )
    g.add( (fb, BRICKFRAME['hasPoint'], pump) )
    g.add( (fb, BRICKFRAME['hasPoint'], supply_temp) )
    g.add( (fb, BRICKFRAME['hasPoint'], return_temp) )
    
    ports = {
        'fb': fb,
        'pi': pi,
        'po': po,
        'si': si,
        'so': so,
    }
    return ports

# instantiate a valve with i inputs and j outputs (usually for 3-way valves)
def gen_ij_valve (prefix, input_count, output_count):
    fb = GTC[prefix+'/fb']
    i  = map(lambda index: GTC[prefix+'/port[i-'+str(index)+']'] , range(input_count))
    ic = map(lambda index: GTC[prefix+'/port[ic-'+str(index)+']'], range(input_count))
    o  = map(lambda index: GTC[prefix+'/port[o-'+str(index)+']'] , range(output_count))
    oc = map(lambda index: GTC[prefix+'/port[oc-'+str(index)+']'], range(output_count))
    
    # types
    g.add( (fb, RDF.type, GTC['IJ_Valve_Functional_Block']) )
    for entity in i:
        g.add( (entity, RDF.type, GTC['IJ_Valve_Input']) )
    for entity in ic:
        g.add( (entity, RDF.type, GTC['IJ_Valve_Input_control']) )
    for entity in o:
        g.add( (entity, RDF.type, GTC['IJ_Valve_Output']) )
    for entity in oc:
        g.add( (entity, RDF.type, GTC['IJ_Valve_Output_control']) )
    
    # isPartOf
    for entity in i+ic+o+oc:
        g.add( (entity, BRICKFRAME['isPartOf'], fb) )
    
    # feeds
    for index in range(input_count):
        g.add( (i[index], BRICKFRAME['feeds'], ic[index]) )
    for input_index in range(input_count):
        for output_index in range(output_count):
            g.add( (ic[input_index], BRICKFRAME['feeds'], oc[output_index]) )
    for index in range(output_count):
        g.add( (oc[index], BRICKFRAME['feeds'], o[index]) )
    
    ports = {
        'fb': fb,
        'i':  i,  # input
        'ic': ic, # inout control
        'o':  o,  # output
        'ic': oc, # output control
    }
    return ports

# instantiates the equivalent of a VAV
def gen_vav (prefix, data, meter, water_system):
    fb                   = GTC[prefix+'/fb']
    ui                   = GTC[prefix+'/port[ui]']
    uo                   = GTC[prefix+'/port[uo]']
    di                   = GTC[prefix+'/port[di]']
    do                   = GTC[prefix+'/port[do]']
    ci                   = GTC[prefix+'/port[ci]']
    co                   = GTC[prefix+'/port[co]']
    zn                   = GTC[prefix+'/port[zn]']
    vav                  = GTC[prefix+'/vav']
    hx                   = gen_hx(prefix+'/hx')
    controller           = GTC[prefix+'/controller']
    supply_damper        = GTC[prefix+'/supply_damper']
    return_damper        = GTC[prefix+'/return_damper']
    upstream_pres        = GTC[prefix+'/upstream_pres']
    downstream_temp      = GTC[prefix+'/downstream_temp']
    cooled_flow          = GTC[prefix+'/cooled_flow']
    cooled_valve         = gen_ij_valve(prefix+'/cooled_valve', 2, 1)
    cooled_valve_command = GTC[prefix+'/cooled_valve_control']
    
    # types
    g.add( (fb                  , RDF.type,   GTC['GTC_VAV_Functional_Block']) )
    g.add( (ui                  , RDF.type,   GTC['GTC_VAV_Upstream_Input']) )
    g.add( (uo                  , RDF.type,   GTC['GTC_VAV_Upstream_Output']) )
    g.add( (di                  , RDF.type,   GTC['GTC_VAV_Downstream_Input']) )
    g.add( (do                  , RDF.type,   GTC['GTC_VAV_Downstream_Output']) )
    g.add( (ci                  , RDF.type,   GTC['GTC_VAV_Cooled_input']) )
    g.add( (co                  , RDF.type,   GTC['GTC_VAV_Cooled_Output']) )
    g.add( (vav                 , RDF.type, BRICK['VAV']) )
#    g.add( (vav                 , RDF.type, BRICK['Variable_Air_Volume']) )
    g.add( (zn                  , RDF.type, BRICK['HVAC_Zone']) )
    g.add( (controller          , RDF.type,   GTC['Controller']) )
    g.add( (supply_damper       , RDF.type, BRICK['Damper']) )
    g.add( (return_damper       , RDF.type, BRICK['Damper']) )
    g.add( (upstream_pres       , RDF.type, BRICK['Pressure_Sensor']) )
    g.add( (downstream_temp     , RDF.type,   GTC['Celcius_Temperature_Sensor']) )
    g.add( (cooled_flow         , RDF.type, BRICK['Chilled_Water_Supply_Flow']) )
    g.add( (cooled_valve_command, RDF.type, BRICK['Cooling_Valve_Command']) )
    
    # labels
    g.add( (supply_damper  , RDFS.label, Literal(data['supply valve'])) )
    g.add( (return_damper  , RDFS.label, Literal(data['return valve'])) )
    g.add( (upstream_pres  , RDFS.label, Literal(data['supply pressure'])) )
    g.add( (hx['fb']       , RDFS.label, Literal(data['cooling coil'])) )
    g.add( (downstream_temp, RDFS.label, Literal(data['supply temperature'])) )
    
    # isPartOf
    g.add( (ui                , BRICKFRAME['isPartOf'], fb) )
    g.add( (uo                , BRICKFRAME['isPartOf'], fb) )
    g.add( (di                , BRICKFRAME['isPartOf'], fb) )
    g.add( (do                , BRICKFRAME['isPartOf'], fb) )
    g.add( (ci                , BRICKFRAME['isPartOf'], fb) )
    g.add( (co                , BRICKFRAME['isPartOf'], fb) )
    g.add( (hx['fb']          , BRICKFRAME['isPartOf'], fb) )
    g.add( (controller        , BRICKFRAME['isPartOf'], fb) )
    g.add( (supply_damper     , BRICKFRAME['isPartOf'], fb) )
    g.add( (return_damper     , BRICKFRAME['isPartOf'], fb) )
    g.add( (upstream_pres     , BRICKFRAME['isPartOf'], fb) )
    g.add( (downstream_temp   , BRICKFRAME['isPartOf'], fb) )
    g.add( (cooled_flow       , BRICKFRAME['isPartOf'], fb) )
    g.add( (cooled_valve['fb'], BRICKFRAME['isPartOf'], fb) )
    g.add( (hx['fb']          , BRICKFRAME['isPartOf'], vav) )
    g.add( (controller        , BRICKFRAME['isPartOf'], vav) )
    g.add( (supply_damper     , BRICKFRAME['isPartOf'], vav) )
    g.add( (return_damper     , BRICKFRAME['isPartOf'], vav) )
    g.add( (upstream_pres     , BRICKFRAME['isPartOf'], vav) )
    g.add( (downstream_temp   , BRICKFRAME['isPartOf'], vav) )
    g.add( (cooled_flow       , BRICKFRAME['isPartOf'], vav) )
    g.add( (cooled_valve['fb'], BRICKFRAME['isPartOf'], vav) )
    g.add( (cooled_flow       , BRICKFRAME['isPartOf'], water_system) )
    
    # feeds
    g.add( (ui                  , BRICKFRAME['feeds'], supply_damper) )
    g.add( (supply_damper       , BRICKFRAME['feeds'], upstream_pres) )
    g.add( (upstream_pres       , BRICKFRAME['feeds'], hx['si']) )
    g.add( (hx['so']            , BRICKFRAME['feeds'], downstream_temp) )
    g.add( (downstream_temp     , BRICKFRAME['feeds'], do) )
    g.add( (di                  , BRICKFRAME['feeds'], return_damper) )
    g.add( (return_damper       , BRICKFRAME['feeds'], uo) )
    g.add( (ci                  , BRICKFRAME['feeds'], cooled_flow) )
    g.add( (cooled_flow         , BRICKFRAME['feeds'], hx['pi']) )
    g.add( (hx['po']            , BRICKFRAME['feeds'], cooled_valve['i'][0]) )
    g.add( (cooled_valve['o'][0], BRICKFRAME['feeds'], co) )
    g.add( (cooled_flow         , BRICKFRAME['feeds'], cooled_valve['i'][1]) )
    g.add( (do                  , BRICKFRAME['feeds'], zn) )
    g.add( (zn                  , BRICKFRAME['feeds'], di) )
    g.add( (vav                 , BRICKFRAME['feeds'], zn) )
    g.add( (zn                  , BRICKFRAME['feeds'], vav) )
    
    # controls
    g.add( (upstream_pres, BRICKFRAME['controls'], controller) )
    g.add( (controller   , BRICKFRAME['controls'], supply_damper) )
    g.add( (controller   , BRICKFRAME['controls'], return_damper) )
    
    # hasPoint
    g.add( (fb                , BRICKFRAME['hasPoint'], supply_damper) )
    g.add( (fb                , BRICKFRAME['hasPoint'], return_damper) )
    g.add( (fb                , BRICKFRAME['hasPoint'], upstream_pres) )
    g.add( (fb                , BRICKFRAME['hasPoint'], downstream_temp) )
    g.add( (fb                , BRICKFRAME['hasPoint'], cooled_flow) )
    g.add( (vav               , BRICKFRAME['hasPoint'], cooled_flow) )
    g.add( (fb                , BRICKFRAME['hasPoint'], cooled_valve['fb']) )
    g.add( (controller        , BRICKFRAME['hasPoint'], meter) )
    g.add( (supply_damper     , BRICKFRAME['hasPoint'], meter) )
    g.add( (return_damper     , BRICKFRAME['hasPoint'], meter) )
    g.add( (upstream_pres     , BRICKFRAME['hasPoint'], meter) )
    g.add( (downstream_temp   , BRICKFRAME['hasPoint'], meter) )
    g.add( (cooled_flow       , BRICKFRAME['hasPoint'], meter) )
    g.add( (vav               , BRICKFRAME['hasPoint'], meter) )
    g.add( (cooled_valve['fb'], BRICKFRAME['hasPoint'], cooled_valve_command) )
    g.add( (vav               , BRICKFRAME['hasPoint'], cooled_valve_command) )
    
    ports = {
        'fb':  fb,
        'ui':  ui,  # upstream input
        'uo':  uo,  # upstream output
        'di':  di,  # downstream input
        'do':  do,  # downstream output
        'ci':  ci,  # cooled input
        'co':  co,  # cooled output
        'zn':  zn,  # zone
        'vav': vav, # the BRICK VAV
    }
    return ports

# instantiate a differential pressure transmitter
def gen_dpt (prefix):
    fb = GTC[prefix+'/fb']
    u  = GTC[prefix+'/port[u]']
    d  = GTC[prefix+'/port[d]']
    o  = GTC[prefix+'/port[o]']
    t  = GTC[prefix+'/transmitter']
    
    # types
    g.add( (fb, RDF.type, GTC['DPT_Functional_Block']) )
    g.add( (u , RDF.type, GTC['DPT_Upstream_Input']) )
    g.add( (d , RDF.type, GTC['DPT_Downstream_Input']) )
    g.add( (o , RDF.type, GTC['DPT_Output']) )
    g.add( (t , RDF.type, GTC['Differential_Pressure_Transmitter']) )
    
    # isPartOf
    g.add( (u, BRICKFRAME['isPartOf'], fb) )
    g.add( (d, BRICKFRAME['isPartOf'], fb) )
    g.add( (o, BRICKFRAME['isPartOf'], fb) )
    g.add( (t, BRICKFRAME['isPartOf'], fb) )
    
    # controls
    g.add( (u, BRICKFRAME['controls'], t) )
    g.add( (d, BRICKFRAME['controls'], t) )
    g.add( (t, BRICKFRAME['controls'], o) )
    
    # hasPoint
    g.add( (fb, BRICKFRAME['hasPoint'], t) )
    
    ports = {
        'fb': fb,
        'u': u, # upstream
        'd': d, # downstream
        'o': o, # transmitter
    }
    return ports

# instantiate a filter element (filter wrapped in a differential pressure transmitter setup)
def gen_filter_element (prefix):
    fb                = GTC[prefix+'/fb']
    i                 = GTC[prefix+'/port[i]']
    o                 = GTC[prefix+'/port[o]']
    input_pressure    = GTC[prefix+'/input_pressure']
    filter_nonkeyword = GTC[prefix+'/filter']
    output_pressure   = GTC[prefix+'/output_pressure']
    dpt               = gen_dpt(prefix+'/dpt')
    
    # types
    g.add( (fb               , RDF.type,   GTC['GTC_Filter_Element_Functional_Block']) )
    g.add( (i                , RDF.type,   GTC['GTC_Filter_Element_Input']) )
    g.add( (o                , RDF.type,   GTC['GTC_Filter_Element_Output']) )
    g.add( (input_pressure   , RDF.type, BRICK['Pressure_Sensor']) )
    g.add( (filter_nonkeyword, RDF.type, BRICK['Filter']) )
    g.add( (output_pressure  , RDF.type, BRICK['Pressure_Sensor']) )
    
    # isPartOf
    g.add( (i                , BRICKFRAME['isPartOf'], fb) )
    g.add( (o                , BRICKFRAME['isPartOf'], fb) )
    g.add( (input_pressure   , BRICKFRAME['isPartOf'], fb) )
    g.add( (filter_nonkeyword, BRICKFRAME['isPartOf'], fb) )
    g.add( (output_pressure  , BRICKFRAME['isPartOf'], fb) )
    g.add( (dpt['fb']        , BRICKFRAME['isPartOf'], fb) )
    
    # feeds
    g.add( (i                , BRICKFRAME['feeds'], input_pressure) )
    g.add( (input_pressure   , BRICKFRAME['feeds'], filter_nonkeyword) )
    g.add( (filter_nonkeyword, BRICKFRAME['feeds'], output_pressure) )
    g.add( (output_pressure  , BRICKFRAME['feeds'], o) )
    
    # controls
    g.add( (input_pressure , BRICKFRAME['controls'], dpt['u']) )
    g.add( (output_pressure, BRICKFRAME['controls'], dpt['d']) )
    
    # hasPoint
    g.add( (fb, BRICKFRAME['hasPoint'], input_pressure) )
    g.add( (fb, BRICKFRAME['hasPoint'], output_pressure) )
    g.add( (fb, BRICKFRAME['hasPoint'], dpt['fb']) )
    
    ports = {
        'fb': fb,
        'i': i,
        'o': o,
    }
    return ports

def gen_room (prefix, room_name, floors, gtc_data, rooms_data, vav_data, metermap):
    fb                = GTC[prefix+'/fb']
    room              = GTC[prefix+'/room']
    radiators         = []
    floor_heaters     = []
    input_dampers     = []
    output_dampers    = []
    override          = GTC[prefix+'/override']
    
    # types
    g.add( (fb      , RDF.type, GTC['GTC_Room_Functional_Block']) )
    g.add( (room    , RDF.type, BRICK['Room']) )
    g.add( (override, RDF.type, GTC['Override_Command']) )
    
    # labels
    g.add( (room, RDFS.label, Literal(room_name)) )
    
    # isPartOf
    g.add( (room, BRICKFRAME['isPartOf'], fb) )
    
    # hasPoint
    g.add( (room, BRICKFRAME['hasPoint'], metermap[rooms_data[room_name]['submeter']]) )
    g.add( (room, BRICKFRAME['hasPoint'], override) )
    
    # temperature
    if 'tr1' in rooms_data[room_name] and rooms_data[room_name]['tr1']!='':
        # sensor
        entity = GTC[prefix+'/temperature_sensor']
        g.add( (entity, RDF.type, GTC['Celcius_Room_Temperature_Sensor']) )
        g.add( (entity, RDFS.label, Literal(rooms_data[room_name]['tr1'])) )
        g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
        g.add( (room  , BRICKFRAME['hasPoint'], entity) )
        g.add( (entity, BRICKFRAME['hasPoint'], metermap[rooms_data[room_name]['submeter']]) )
        
        # setpoint: Comfort temperature setpoint 1
        entity = GTC[prefix+'/temperature_setpoint_comfort1']
        g.add( (entity, RDF.type, GTC['Celcius_Room_Temperature_Setpoint']) )
        g.add( (entity, RDFS.label, Literal('Comfort temperature setpoint 1')) )
        g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
        g.add( (room  , BRICKFRAME['hasPoint'], entity) )
        g.add( (entity, BRICKFRAME['hasPoint'], metermap[rooms_data[room_name]['submeter']]) )
        
        # setpoint: Comfort temperature setpoint 2
        entity = GTC[prefix+'/temperature_setpoint_comfort2']
        g.add( (entity, RDF.type, GTC['Celcius_Room_Temperature_Setpoint']) )
        g.add( (entity, RDFS.label, Literal('Comfort temperature setpoint 2')) )
        g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
        g.add( (room  , BRICKFRAME['hasPoint'], entity) )
        g.add( (entity, BRICKFRAME['hasPoint'], metermap[rooms_data[room_name]['submeter']]) )
        
        # setpoint: Night temperature setpoint 1
        entity = GTC[prefix+'/temperature_setpoint_night1']
        g.add( (entity, RDF.type, GTC['Celcius_Room_Temperature_Setpoint']) )
        g.add( (entity, RDFS.label, Literal('Night temperature setpoint 1')) )
        g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
        g.add( (room  , BRICKFRAME['hasPoint'], entity) )
        g.add( (entity, BRICKFRAME['hasPoint'], metermap[rooms_data[room_name]['submeter']]) )
        
        # setpoint: Night temperature setpoint 2
        entity = GTC[prefix+'/temperature_setpoint_night2']
        g.add( (entity, RDF.type, GTC['Celcius_Room_Temperature_Setpoint']) )
        g.add( (entity, RDFS.label, Literal('Night temperature setpoint 2')) )
        g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
        g.add( (room  , BRICKFRAME['hasPoint'], entity) )
        g.add( (entity, BRICKFRAME['hasPoint'], metermap[rooms_data[room_name]['submeter']]) )
        
        # setpoint: Standby temperature setpoint 1
        entity = GTC[prefix+'/temperature_setpoint_standby1']
        g.add( (entity, RDF.type, GTC['Celcius_Room_Temperature_Setpoint']) )
        g.add( (entity, RDFS.label, Literal('Standby temperature setpoint 1')) )
        g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
        g.add( (room  , BRICKFRAME['hasPoint'], entity) )
        g.add( (entity, BRICKFRAME['hasPoint'], metermap[rooms_data[room_name]['submeter']]) )
        
        # setpoint: Standby temperature setpoint 2
        entity = GTC[prefix+'/temperature_setpoint_standby2']
        g.add( (entity, RDF.type, GTC['Celcius_Room_Temperature_Setpoint']) )
        g.add( (entity, RDFS.label, Literal('Standby temperature setpoint 2')) )
        g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
        g.add( (room  , BRICKFRAME['hasPoint'], entity) )
        g.add( (entity, BRICKFRAME['hasPoint'], metermap[rooms_data[room_name]['submeter']]) )
        
        # heating deadband
        entity = GTC[prefix+'/temperature_heating_deadband']
        g.add( (entity, RDF.type, BRICK['Heating_Discharge_Air_Temperature_Dead_Band_setpoint']) )
        g.add( (room  , BRICKFRAME['hasPoint'], entity) )
        g.add( (entity, BRICKFRAME['hasPoint'], metermap[rooms_data[room_name]['submeter']]) )
        
        # cooling deadband
        entity = GTC[prefix+'/temperature_cooling_deadband']
        g.add( (entity, RDF.type, BRICK['Cooling_Discharge_Air_Temperature_Dead_Band_setpoint']) )
        g.add( (room  , BRICKFRAME['hasPoint'], entity) )
        g.add( (entity, BRICKFRAME['hasPoint'], metermap[rooms_data[room_name]['submeter']]) )
        
    
    # CO2
    if 'co2' in rooms_data[room_name] and rooms_data[room_name]['co2']!='':
        # sensor
        entity = GTC[prefix+'/co2_sensor']
        g.add( (entity, RDF.type, BRICK['CO2_Sensor']) )
        g.add( (entity, RDFS.label, Literal(rooms_data[room_name]['co2'])) )
        g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
        g.add( (room  , BRICKFRAME['hasPoint'], entity) )
        g.add( (entity, BRICKFRAME['hasPoint'], metermap[rooms_data[room_name]['submeter']]) )
        
        # setpoint
        entity = GTC[prefix+'/co2_setpoint']
        g.add( (entity, RDF.type, BRICK['CO2_Setpoint']) )
        g.add( (entity, RDFS.label, Literal(rooms_data[room_name]['co2'])) )
        g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
        g.add( (room  , BRICKFRAME['hasPoint'], entity) )
        g.add( (entity, BRICKFRAME['hasPoint'], metermap[rooms_data[room_name]['submeter']]) )
    
    # PIR sensor
    if 'pir' in rooms_data[room_name] and rooms_data[room_name]['pir']!='':
        entity = GTC[prefix+'/pir']
        g.add( (entity, RDF.type, BRICK['Occupancy_Sensor']) )
        g.add( (entity, RDFS.label, Literal(rooms_data[room_name]['pir'])) )
        g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
        g.add( (room, BRICKFRAME['hasPoint'], entity) )
        g.add( (entity, BRICKFRAME['hasPoint'], metermap[rooms_data[room_name]['submeter']]) )
    
    # radiators
    if 'radiators' in rooms_data[room_name] and rooms_data[room_name]['radiators']['count']>0:
        for index in range(rooms_data[room_name]['radiators']['count']):
            entity = GTC[prefix+'/radiators/'+str(index)]
            g.add( (entity, RDFS.label, Literal(rooms_data[room_name]['radiators']['id'])) )
            g.add( (entity, RDF.type, BRICK['Radiator']) )
            g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
            radiators.append(entity)
    
    # floor heaters
    if 'floorheating' in rooms_data[room_name] and rooms_data[room_name]['floorheating']['count']>0:
        for index in range(rooms_data[room_name]['floorheating']['count']):
            entity = GTC[prefix+'/floorheaters/'+str(index)]
            g.add( (entity, RDFS.label, Literal(rooms_data[room_name]['floorheating']['id'])) )
            g.add( (entity, RDF.type, GTC['FloorHeater']) )
            g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
            floor_heaters.append(entity)
    
    # input dampers
    if 'input dampeners' in rooms_data[room_name] and rooms_data[room_name]['input dampeners']['count']>0:
        for index in range(rooms_data[room_name]['input dampeners']['count']):
            entity = GTC[prefix+'/input_dampers/'+str(index)]
            g.add( (entity, RDFS.label, Literal(rooms_data[room_name]['input dampeners']['id'])) )
            g.add( (entity, RDF.type, BRICK['Damper']) )
            g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
            g.add( (entity, BRICKFRAME['hasPoint'], metermap[rooms_data[room_name]['submeter']]) )
            input_dampers.append(entity)
    
    # output dampers
    if 'output dampeners' in rooms_data[room_name] and rooms_data[room_name]['output dampeners']['count']>0:
        for index in range(rooms_data[room_name]['output dampeners']['count']):
            entity = GTC[prefix+'/output_dampers/'+str(index)]
            g.add( (entity, RDFS.label, Literal(rooms_data[room_name]['output dampeners']['id'])) )
            g.add( (entity, RDF.type, BRICK['Damper']) )
            g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
            g.add( (entity, BRICKFRAME['hasPoint'], metermap[rooms_data[room_name]['submeter']]) )
            output_dampers.append(entity)
    
    # lighting
    index = 0
    zone_index = 0
    for group in rooms_data[room_name]['lighting']:
        lighting_zone = GTC[prefix+'/lighting_zone/'+str(zone_index)]
        g.add( (lighting_zone, RDF.type, BRICK['Lighting_Zone']) )
        g.add( (lighting_zone, BRICKFRAME['contains'], room) )
#        g.add( (lighting_zone, BRICKFRAME['feeds'], room) )
        
        command = GTC[prefix+'/lighting_zone/'+str(zone_index)+'_status']
        g.add( (command, RDFS.label, Literal(group['id'])) )
        g.add( (command, RDF.type, BRICK['Luminance_Status']) )
        g.add( (lighting_zone, BRICKFRAME['hasPoint'], command) )
        
        command = GTC[prefix+'/lighting_zone/'+str(zone_index)+'_command']
        g.add( (command, RDFS.label, Literal(group['id'])) )
        g.add( (command, RDF.type, BRICK['Luminance_Command']) )
        g.add( (lighting_zone, BRICKFRAME['hasPoint'], command) )
        floors
        zone_index += 1
        
        if group['type']=='ledgo':
            g.add( (lighting_zone, RDFS.label, Literal('LEDGO')) )
            
            for i in range(group['count']):
                entity = GTC[prefix+'/lighting/'+str(index)]
                g.add( (entity, RDFS.label, Literal(group['id'])) )
                g.add( (entity, RDF.type, GTC['LEDGO_Lighting_System']) )
                g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
                g.add( (entity, BRICKFRAME['isPartOf'], room) )
                g.add( (entity, BRICKFRAME['hasPoint'], metermap[rooms_data[room_name]['submeter']]) )
                g.add( (entity, BRICKFRAME['feeds'], lighting_zone) )
                g.add( (entity, BRICKFRAME['feeds'], room) )
                index += 1
        else:
            print('Error: Unknown type ('+group['type']+') of lighting for room '+room_name+'. Skipping ...')
    
    ports = {
        'fb':            fb,
        'room':          room,
        'floor':         rooms_data[room_name]['floor'],
        'radiators':     radiators,
        'floorheaters':  floor_heaters,
        'inputdampers':  input_dampers,
        'outputdampers': output_dampers,
    }
    return ports

def gen_foyer_room (prefix, metermap):
    fb                = GTC[prefix+'/fb']
    room              = GTC[prefix+'/room']
    floor_heaters     = []
    
    # types
    g.add( (fb, RDF.type, GTC['GTC_Room_Functional_Block']) )
    g.add( (room, RDF.type, BRICK['Room']) )
    
    # labels
    g.add( (room, RDFS.label, Literal('1.A.14')) )
    
    # isPartOf
    g.add( (room, BRICKFRAME['isPartOf'], fb) )
    
    # hasPoint
    g.add( (room, BRICKFRAME['hasPoint'], metermap['-A1']) )
    
    # temperature sensor
    temperature_sensors = ['-01-ZV01-1A14-TR01', '-01-ZV02-1A14-TR01', '-01-ZV03-1A14-TR01']
    for index in range(len(temperature_sensors)):
        entity = GTC[prefix+'/temperature/'+str(index)]
        g.add( (entity, RDF.type, GTC['Celcius_Temperature_Sensor']) )
        g.add( (entity, RDFS.label, Literal(temperature_sensors[index])) )
        g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
        g.add( (entity, BRICKFRAME['hasPoint'], room) )
        g.add( (entity, BRICKFRAME['hasPoint'], metermap['-A1']) )
    
    # CO2 sensor
    co2_sensors = ['-01-ZV01-1A14-CO2', '-01-ZV02-1A14-CO2', '-01-ZV03-1A14-CO2']
    for index in range(len(co2_sensors)):
        entity = GTC[prefix+'/co2/'+str(index)]
        g.add( (entity, RDF.type, BRICK['CO2_Sensor']) )
        g.add( (entity, RDFS.label, Literal(co2_sensors[index])) )
        g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
        g.add( (entity, BRICKFRAME['hasPoint'], room) )
        g.add( (entity, BRICKFRAME['hasPoint'], metermap['-A1']) )
    
    # floor heaters
    fh_sensors = [('-01-1F14-MV01', 1), ('-01-ZV01-1A14-MV1-02', 2), ('-01-ZV02-1A14-MV1-03', 3), ('-01-ZV03-1A14-MV1-02', 2)]
    for sensor_index in range(len(fh_sensors)):
        for index in range(fh_sensors[sensor_index][1]):
            entity = GTC[prefix+'/floorheaters/'+str(index)+'-'+str(fh_sensors[sensor_index][1])]
            g.add( (entity, RDFS.label, Literal(fh_sensors[sensor_index][0])) )
            g.add( (entity, RDF.type, GTC['FloorHeater']) )
            g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
            g.add( (room, BRICKFRAME['hasPoint'], entity) )
            floor_heaters.append(entity)
    
    # horizontal windows
    for i in range(6):
        entity = GTC[prefix+'/horizontal_windows/'+str(index)]
        g.add( (entity, RDFS.label, Literal('-01-1A14-VI01')) )
        g.add( (entity, RDF.type, GTC['Horizontal_Window_Actuator']) )
        g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
        g.add( (room, BRICKFRAME['hasPoint'], entity) )
        g.add( (entity, BRICKFRAME['hasPoint'], metermap['-A1']) )
    
    # vertical windows
    for i in range(4):
        entity = GTC[prefix+'/vertical_windows/'+str(index)]
        g.add( (entity, RDFS.label, Literal('-01-1A14-VI01')) )
        g.add( (entity, RDF.type, GTC['Vertical_Window_Actuator']) )
        g.add( (entity, BRICKFRAME['isLocatedIn'], room) )
        g.add( (room, BRICKFRAME['hasPoint'], entity) )
        g.add( (entity, BRICKFRAME['hasPoint'], metermap['-A1']) )
    
    ports = {
        'fb':            fb,
        'room':          room,
        'floor':         0,
        'radiators':     [],
        'floorheaters':  floor_heaters,
        'inputdampers':  [],
        'outputdampers': [],
    }
    return ports

def gen_misc (prefix, floors):
    pass

def gen_building (prefix):
    # load data
    with open('gtc.json') as fo:
        gtc_data = json.loads(''.join(fo.readlines()))
    with open('rooms.json') as fo:
        rooms_data = json.loads(''.join(fo.readlines()))
    with open('gtc_vavs.json') as fo:
        vavs_data = json.loads(''.join(fo.readlines()))
    
    building             = GTC[prefix]
    floors               = map(lambda level: GTC[prefix+'/floors/'+str(level)], range(3))
    chilled_water_system = GTC[prefix+'/systems/water/chilled']
    electrical           = gen_electrical(prefix+'/electrical', floors)
    metermap = electrical['metermap']
    rooms                = {}
    for room_name in rooms_data.keys():
        rooms[room_name] = gen_room(prefix+'/rooms/'+room_name, room_name, floors, gtc_data, rooms_data, vavs_data, metermap)
    rooms['1.A.14'] = gen_foyer_room(prefix+'/rooms/1.A.14', metermap)
    vavs                 = []
    for index in range(len(vavs_data)):
        vav_data = vavs_data[index]
        vav = gen_vav(prefix+'/vavs/'+str(index), vav_data, metermap['-A1'], chilled_water_system)
        vavs.append(vav)
    district_meter       = gen_heating_power_meter(prefix+'/district_meter')
    radiator_htb         = gen_heat_transfer_box(prefix+'/radiator_htb')
    floor_htb            = gen_heat_transfer_box(prefix+'/floor_htb')
    ahu                  = GTC[prefix+'/ahu']
    outside_temp         = GTC[prefix+'/outside_temp']
    outside_fe           = gen_filter_element(prefix+'outside_fe')
    outside_fe_temp      = GTC[prefix+'/outside_fe_temp']
    hx1                  = gen_hx(prefix+'/district_hx')
    hx_temp              = GTC[prefix+'/hx_temp']
    hx_fan               = GTC[prefix+'/']
    hx2                  = gen_hx(prefix+'/return_hx')
    supply_temp          = GTC[prefix+'/supply_temp']
    supply_n_pres        = GTC[prefix+'/supply_north_pressure']
    supply_s_pres        = GTC[prefix+'/supply_south_pressure']
    return_n_pres        = GTC[prefix+'/return_north_pressure']
    return_s_pres        = GTC[prefix+'/return_south_pressure']
    return_damper        = GTC[prefix+'/damper']
    return_fe            = gen_filter_element(prefix+'return_fe')
    return_fe_temp       = GTC[prefix+'/return_fe_temp']
    exhaust_temp         = GTC[prefix+'/exhaust_temp']
    exhaust_fan          = GTC[prefix+'/exhaust_fan']
    ahu_meter            = gen_heating_power_meter(prefix+'ahu_meter')
    district_supply_temp = GTC[prefix+'/district_supply_temp']
    district_pump        = GTC[prefix+'/district_pump']
    district_return_temp = GTC[prefix+'/district_return_temp']
    district_valve       = GTC[prefix+'/district_valve']
    district_rect        = GTC[prefix+'/district_rectifier']
    wind_dir             = GTC[prefix+'/wind_direction']
    wind_spd             = GTC[prefix+'/wind_speed']
    
    # misc
    gen_misc(prefix+'/misc', floors)
    
    # convenience maps
    supply_map = {'N': supply_n_pres, 'S': supply_s_pres}
    return_map = {'N': return_n_pres, 'S': return_s_pres}
    
    # labels
    g.add( (building, RDFS.label, Literal("GreenTech Center in Vejle, Denmark")) )
    
    # types
    g.add( (chilled_water_system, RDF.type, BRICK['CWS']) )
    g.add( (building            , RDF.type, BRICK['Building']) )
    for floor in floors:
        g.add( (floor           , RDF.type, BRICK['Floor']) )
    g.add( (ahu                 , RDF.type, BRICK['AHU']) )
    g.add( (outside_temp        , RDF.type,   GTC['Celcius_Temperature_Sensor']) )
    g.add( (outside_fe_temp     , RDF.type,   GTC['Celcius_Temperature_Sensor']) )
    g.add( (hx_temp             , RDF.type,   GTC['Celcius_Temperature_Sensor']) )
    g.add( (hx_fan              , RDF.type, BRICK['Fan']) )
    g.add( (supply_temp         , RDF.type,   GTC['Celcius_Temperature_Sensor']) )
    g.add( (supply_n_pres       , RDF.type, BRICK['Pressure_Sensor']) )
    g.add( (supply_s_pres       , RDF.type, BRICK['Pressure_Sensor']) )
    g.add( (return_n_pres       , RDF.type, BRICK['Pressure_Sensor']) )
    g.add( (return_s_pres       , RDF.type, BRICK['Pressure_Sensor']) )
    g.add( (return_damper       , RDF.type, BRICK['Damper']) )
    g.add( (return_fe_temp      , RDF.type,   GTC['Celcius_Temperature_Sensor']) )
    g.add( (exhaust_temp        , RDF.type,   GTC['Celcius_Temperature_Sensor']) )
    g.add( (exhaust_fan         , RDF.type, BRICK['Fan']) )
    g.add( (district_supply_temp, RDF.type,   GTC['Celcius_Temperature_Sensor']) )
    g.add( (district_pump       , RDF.type, BRICK['Pump']) )
    g.add( (district_return_temp, RDF.type,   GTC['Celcius_Temperature_Sensor']) )
    g.add( (district_valve      , RDF.type, BRICK['Valve']) )
    g.add( (district_rect       , RDF.type,   GTC['Rectifier']) )
    g.add( (wind_dir            , RDF.type,   GTC['Wind_Direction_Sensor']) )
    g.add( (wind_spd            , RDF.type,   GTC['Wind_Speed_Sensor']) )
    
    # feeds
    g.add( (district_meter['metered_supply'], BRICKFRAME['feeds'], radiator_htb['pi']) )
    g.add( (district_meter['metered_supply'], BRICKFRAME['feeds'],    floor_htb['pi']) )
    g.add( (district_meter['metered_supply'], BRICKFRAME['feeds'],    ahu_meter['supply']) )
    g.add( ( radiator_htb['pi'], BRICKFRAME['feeds'], ahu_meter['metered_return']) )
    g.add( (    floor_htb['pi'], BRICKFRAME['feeds'], ahu_meter['metered_return']) )
    g.add( (ahu_meter['return'], BRICKFRAME['feeds'], ahu_meter['metered_return']) )
    for vav in vavs:
        g.add( (ahu, BRICKFRAME['feeds'], vav['vav']) )
    for room_name in rooms:
        room = rooms[room_name]
        for radiator in room['radiators']:
            g.add( (radiator_htb['so'], BRICKFRAME['feeds'], radiator) )
            g.add( (radiator          , BRICKFRAME['feeds'], radiator_htb['so']) )
    for room_name in rooms:
        room = rooms[room_name]
        for floor_heater in room['floorheaters']:
            g.add( (floor_htb['so'], BRICKFRAME['feeds'], floor_heater) )
            g.add( (floor_heater   , BRICKFRAME['feeds'], floor_htb['so']) )
    for index in range(len(vavs_data)):
        vav_data = vavs_data[index]
        vav = vavs[index]
        
        # upstream
        g.add( (supply_map[vav_data['side']], BRICKFRAME['feeds'], vav['ui']) )
        g.add( (vav['uo']                   , BRICKFRAME['feeds'], return_map[vav_data['side']]) )
        
        # downstream
        for room_name in vav_data['rooms']:
            room = rooms[room_name]
            for damper in room['inputdampers']:
                g.add( (vav['zn'], BRICKFRAME['feeds'], damper) )
            for damper in room['outputdampers']:
                g.add( (damper   , BRICKFRAME['feeds'], vav['zn']) )
    g.add( (outside_temp               , BRICKFRAME['feeds'], outside_fe['i']) )
    g.add( (outside_fe['o']            , BRICKFRAME['feeds'], outside_fe_temp) )
    g.add( (outside_fe_temp            , BRICKFRAME['feeds'], hx1['si']) )
    g.add( (hx1['so']                  , BRICKFRAME['feeds'], hx_temp) )
    g.add( (hx_temp                    , BRICKFRAME['feeds'], hx_fan) )
    g.add( (hx_fan                     , BRICKFRAME['feeds'], hx2['si']) )
    g.add( (hx2['so']                  , BRICKFRAME['feeds'], supply_temp) )
    g.add( (supply_temp                , BRICKFRAME['feeds'], supply_n_pres) )
    g.add( (supply_temp                , BRICKFRAME['feeds'], supply_n_pres) )
    g.add( (return_n_pres              , BRICKFRAME['feeds'], return_damper) )
    g.add( (return_s_pres              , BRICKFRAME['feeds'], return_damper) )
    g.add( (return_damper              , BRICKFRAME['feeds'], return_fe['i']) )
    g.add( (return_fe['o']             , BRICKFRAME['feeds'], return_fe_temp) )
    g.add( (return_fe_temp             , BRICKFRAME['feeds'], hx1['pi']) )
    g.add( (hx1['po']                  , BRICKFRAME['feeds'], exhaust_temp) )
    g.add( (exhaust_temp               , BRICKFRAME['feeds'], exhaust_fan) )
    g.add( (ahu_meter['metered_supply'], BRICKFRAME['feeds'], district_supply_temp) )
    g.add( (district_supply_temp       , BRICKFRAME['feeds'], district_pump) )
    g.add( (district_pump              , BRICKFRAME['feeds'], hx2['pi']) )
    g.add( (hx2['po']                  , BRICKFRAME['feeds'], district_return_temp) )
    g.add( (district_return_temp       , BRICKFRAME['feeds'], district_valve) )
    g.add( (district_valve             , BRICKFRAME['feeds'], ahu_meter['metered_return']) )
    g.add( (district_return_temp       , BRICKFRAME['feeds'], district_rect) )
    g.add( (district_rect              , BRICKFRAME['feeds'], district_supply_temp) )
    
    # isPartOf
    for floor in floors:
        g.add( (floor           , BRICKFRAME['isPartOf'], building) )
    for room_name in rooms:
        g.add( (rooms[room_name]['fb'], BRICKFRAME['isPartOf'], floors[rooms[room_name]['floor']]) )
    g.add( (district_meter['fb'], BRICKFRAME['isPartOf'], building) )
    g.add( (radiator_htb['fb']  , BRICKFRAME['isPartOf'], building) )
    g.add( (floor_htb['fb']     , BRICKFRAME['isPartOf'], building) )
    g.add( (outside_temp        , BRICKFRAME['isPartOf'], building) )
    g.add( (outside_fe['fb']    , BRICKFRAME['isPartOf'], building) )
    g.add( (outside_fe_temp     , BRICKFRAME['isPartOf'], building) )
    g.add( (hx1['fb']           , BRICKFRAME['isPartOf'], building) )
    g.add( (hx_temp             , BRICKFRAME['isPartOf'], building) )
    g.add( (hx_fan              , BRICKFRAME['isPartOf'], building) )
    g.add( (hx2['fb']           , BRICKFRAME['isPartOf'], building) )
    g.add( (supply_temp         , BRICKFRAME['isPartOf'], building) )
    g.add( (supply_n_pres       , BRICKFRAME['isPartOf'], building) )
    g.add( (supply_s_pres       , BRICKFRAME['isPartOf'], building) )
    g.add( (return_n_pres       , BRICKFRAME['isPartOf'], building) )
    g.add( (return_s_pres       , BRICKFRAME['isPartOf'], building) )
    g.add( (return_damper       , BRICKFRAME['isPartOf'], building) )
    g.add( (return_fe['fb']     , BRICKFRAME['isPartOf'], building) )
    g.add( (return_fe_temp      , BRICKFRAME['isPartOf'], building) )
    g.add( (exhaust_temp        , BRICKFRAME['isPartOf'], building) )
    g.add( (exhaust_fan         , BRICKFRAME['isPartOf'], building) )
    g.add( (ahu_meter['fb']     , BRICKFRAME['isPartOf'], building) )
    g.add( (district_supply_temp, BRICKFRAME['isPartOf'], building) )
    g.add( (district_pump       , BRICKFRAME['isPartOf'], building) )
    g.add( (district_return_temp, BRICKFRAME['isPartOf'], building) )
    g.add( (district_valve      , BRICKFRAME['isPartOf'], building) )
    g.add( (district_rect       , BRICKFRAME['isPartOf'], building) )
    
    # hasPart
    for index in range(len(vavs_data)):
        vav_data = vavs_data[index]
        vav = vavs[index]
        for room_name in vav_data['rooms']:
            room = rooms[room_name]
            g.add( (vav['zn'], BRICKFRAME['hasPart'], room['room']) )
            g.add( (room['room'], BRICKFRAME['isPartOf'], vav['zn']) )
#            print((vav['zn'], BRICKFRAME['hasPart'], room['room']))
    
    # hasPoint: metering
    entities = [
        district_meter['fb'],
        radiator_htb['fb'],
        floor_htb['fb'],
        outside_temp,
        outside_fe['fb'],
        outside_fe_temp,
        hx1['fb'],
        hx_temp,
        hx_fan,
        hx2['fb'],
        supply_temp,
        supply_n_pres,
        supply_s_pres,
        return_n_pres,
        return_s_pres,
        return_damper,
        return_fe['fb'],
        return_fe_temp,
        exhaust_temp,
        exhaust_fan,
        ahu_meter['fb'],
        district_supply_temp,
        district_pump,
        district_return_temp,
        district_valve,
        district_rect,
    ]
    entity_points = [
        outside_temp,
        outside_fe_temp,
        hx_temp,
        hx_fan,
        supply_temp,
        supply_n_pres,
        supply_s_pres,
        return_n_pres,
        return_s_pres,
        return_damper,
        return_fe_temp,
        exhaust_temp,
        exhaust_fan,
        district_supply_temp,
        district_pump,
        district_return_temp,
        district_valve,
        district_rect,
    ]
    for vav in vavs:
        g.add( (vav['vav'], BRICKFRAME['hasPoint'], metermap['-A1']) )
    for entity in entities:
        g.add( (entity , BRICKFRAME['hasPoint'], metermap['-A1']) )
    for entity in entity_points:
        g.add( (ahu , BRICKFRAME['hasPoint'], entity) )
    g.add( (building , BRICKFRAME['hasPoint'], wind_dir) )
    g.add( (building , BRICKFRAME['hasPoint'], wind_spd) )
    

################################################################################
###################################################################### main ####
################################################################################

prefix = 'building:gtc'

gen_extensions()

# building
b = gen_building(prefix)

################################################################################
############################################################### back matter ####
################################################################################

g.serialize('gtc_brick.ttl', 'turtle')

