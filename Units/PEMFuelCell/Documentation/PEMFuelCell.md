Exergetic aspects
Exergy method of analyzing energy systems integrates the first and second law of thermodynamics and reference environmental conditions. Exergy is defined as the maximum amount of work which can be obtained from a system or a flow of matter when it is brought reversibly to equilibrium with the reference environment. Every substance or system not in equilibrium with its reference environment has some quantity of exergy, while a substance or system in equilibrium with its reference environment has no exergy since it has no ability to cause any change with respect to its reference environment. The exergy consumption during a process is proportional to the entropy production due to irreversibilities. It is a useful tool for furthering the goal of more efficient energy use, as it enables the determination of the location, type and true magnitude of energy wastes and losses in a system [3].
Exergy of a stream of matter can be divided into different components. In the absence of nuclear, magnetism, electricity and surface tension effects, the specific total exergy is the sum of:
where exke , expe , extm and exch are the kinetic exergy, potential exergy, thermomechanical exergy and chemical exergy, respectively. Since the changes in the kinetic and gravitational potential energies are considered to be negligible in the present study, physical exergy, which is the sum of kinetic, potential and thermomechanical exergies, reduces to thermomechanical exergy only.
$ex=ex_{ke}+ex_{pe}+ex_{tm}+ex_{ch}$

The specific thermomechanical exergy at a given state is defined as follows:
$ex_{tm}=(h-h_{0})-T_{0}(s-s_{0})$
where h and s refer to specific enthalpy and entropy, respectively, at a given state. The subscript 0 represents the conditions of the reference environment (restricted).

The chemical exergy is a result of compositional imbalance between a substance and its reference environment. Ona molar basis, the specific chemical exergy of a substancecan be written as follows: 
$ex_{ch}=\sum_{j}x_{j}(\mu_{j0}-\mu_{j00})$
where xj is the mole fraction of the species j in the flow, µj 0 is the chemical potential of species j in the flow evaluated at T0 and P0 and µj 00 is the chemical potential of species j in the flow evaluated in the reference environment (unrestricted).


The reference environment
Exergy analysis cannot be performed without defining the reference environment. Moreover, in dealing with reacting systems, two forms of equilibrium has to be defined, the environmental (restricted) state and the dead (unrestricted) state. The environmental state is a restricted equilibrium where the conditions of mechanical (P ) and thermal (T ) are satisfied. The dead state is an unrestricted equilibrium where the conditions of mechanical (P ), thermal (T ) and chemical potential (µ) are satisfied.
In the present study, restricted dead state is defined as STP condition (298 K and 1 atm), whereas the unrestricted dead state is defined (Table 1) as the composition of wet atmospheric air with relative humidity of 57.5%, which can be taken as a typical annual average [8].

Table 1


Fuel cell power system
The PEM fuel cell power system considered in the present study is based on Ballard’s fuel cell engine for light-duty vehicles and is shown in Fig. 1. The power system consists of two modules: the PEM fuel cell stack module and system module, and a cooling pump. The main components of the system module are air compressor, heat exchanger, humidifier and the cooling loop. The PEM fuel cell stack module is the heart of the power system where pressurized, humidified air and hydrogen are supplied from the system module. This is the place where electrical power is produced through electrochemical reaction of hydrogen and oxygen as follows:
$H_{2(g)}+{\frac{1}{2}}O_{2(g)}\Longrightarrow H_{2}O_{(l)}+electrical power + waste heat$
Here, the waste heat produced in the stack module is removed through the cooling loop. The air compressor component of the system module provides pressurized oxygen in the form of air, to the stack. The pressurized air is cooled down in a heat exchanger and humidified in a humidifier before being fed to the stack. Similarly, compressed hydrogen stored on-board is humidified in a humidifier before feeding to the stack. Humidification of inlet streams is necessary to prevent dehydration of the membranes in the fuel cell stack. Not all the hydrogen supplied to the fuel cell is consumed by the fuel cell stack, and therefore the unreacted hydrogen leaving the stack is recirculated.

The air compressor component of the system module provides pressurized oxygen in the form of air, to the stack. The pressurized air is cooled down in a heat exchanger and humidified in a humidifier before being fed to the stack. Similarly, compressed hydrogen stored on-board is humidified in a humidifier before feeding to the stack. Humidification of inlet streams is necessary to prevent dehydration of the membranes in the fuel cell stack. Not all the hydrogen supplied to the fuel cell is consumed by the fuel cell stack, and therefore the unreacted hydrogen leaving the stack is recirculated.
The purpose of the cooling loop is to remove the heat produced by the exothermic reaction of hydrogen and oxygen. The cooling loop consists of a radiator, cooling pump, radiator fan. The cooling pump directs coolant (water/glycol) through the stack to remove the waste heat via radiator.


PEM fuel cell performance model
Here, the PEM fuel cell performance model developed by Baschuk and Li is used to simulate the fuel cell stack. The model predicts the voltage of a single cell at any specified operating conditions. The voltage of the entire stack is then obtained by multiplying the single cell potential with the number of cells in the stack. The output voltage of a fuel cell can be represented as
$E_{I}=E_{r}-E_{irr}$
where Er is the reversible voltage of the cell and Eirr is the irreversible voltage loss or overpotential due to catalyst layers, electron migration in the bipolar plates and electrode backing, and proton migration in the polymer electrolyte membrane.

Reversible cell voltage (Er)
The reversible cell voltage is the cell potential obtained at thermodynamic reversible condition. It is given by the following expression:
$E_{r}=1.299+0.85\times10^{-3}(T-295.15)+4.31\times10^{-5}T \ln\left[\left(\frac{C_{H_{2}}}{22.22}\right)\left(\frac{C_{0_{2}}}{7.033}\right)^{1/2}\right]$

Irreversible cell voltage loss or overpotential (Eirr)
Irreversible cell voltage loss or overpotential is composed of activation overpotential (ηact ) due to catalyst layers, ohmic overpotential (ηohmic ) due to electron migration in the bipolar plates and electrode backing, and proton migration in the polymer electrolyte membrane, and concentration overpotential (ηcon ) due to the mass transfer limitations at higher current densities.
$E_{irr}=\eta_{act}+\eta_{ohmic}+\eta_{con}$

Activation overpotential (ηact)
Activation overpotential is due to the catalyst layers. It takes into account the electrochemical kinetics, and electron and proton migration, and is composed of both the anode and cathode catalyst layer activation overpotentials:
$\eta_{act}=\eta_{act}^{a}+\eta_{act}^{c}$
where \eta_{act}^{a} and \eta_{act}^{c} are the activation overpotentials in the anode and cathode catalysts layers, respectively.

Ohmic overpotential (ηohmic)
The ohmic overpotential is given by the following expression:
$\eta_{ohmic}=\eta_{bp}^{a}+\eta_{bp}^{c}+\eta_{e}^{a}+\eta_{e}^{c}+\eta_{m}$
where \eta_{bp}^{a} and \eta_{bp}^{c} are the ohmic losses of the anode and cathode bipolar plates, respectively. The ohmic losses of the anode and cathode electrode backing layers are denoted by \eta_{e}^{a} and \eta_{e}^{c}. The overpotential due to the polymer electrolyte membrane is \eta_{m}. The detailed descriptions and expressions for these overpotentials can be found elsewhere.

Concentration overpotential (ηcon)
It is due to mass transfer limitations at higher current
densities, and is composed of both the anode and cathode
concentration overpotentials:

$\eta_{con}=\eta_{con}^{a}+\eta_{con}^{c}$
where \eta_{con}^{a} and \eta_{con}^{c} are the anode and cathode concentration overpotential, respectively.

Stack power (Ẇstack)
The power produced by a single cell is given as:
$\dot{W}_{cell}=E(I)\times I\times A_{cell}$
where I is the current density and Acell is the geometric area of the cell. The stack power is then obtained by multiplying the single cell power with number of cells in the stack, which can be written as:
${\dot{W}}_{stack}=n_{fc}\times{\dot{W}}_{cell}$
where nfc is the number of fuel cells in the stack. In the present power system, we consider 97 cells of 900 cm² geometric area in the stack producing net system power of 68 kW at I = 1.15 A·cm¯² and E = 0.78 V.


Assumptions
The assumptions considered in the analysis are as follows:
• The hydrogen storage cylinder or tank is at a constant pressure of 10 bar and temperature of 298 K.
• Isentropic efficiencies of compressor, cooling pump and radiator fan are assumed to be 70%.
• 20% of the total heat produced by the fuel cell stack is assumed to be lost due to convection and radiation.
• The temperatures at the inlet and outlet of the coolant circulation pump are assumed to be equal.
• The environmental (restricted) state is at STP conditions, i.e., 298 K and 1 atm.
• Wet atmospheric air with the composition given in Table 1 is used as dead (unrestricted) state.
The net system power produced by the fuel cell power system is obtained by deducting the parasitic loads from the gross stack power. For the present system, net system power becomes
Ẇnet = Ẇstack − Ẇac − Ẇcp − Ẇrf
where Ẇstack , Ẇac , Ẇcp and Ẇrf denotes stack power, power input to air compressor, cooling pump and radiator fan, respectively. The governing thermodynamic first and second law equations are combined for the system as well as for individual components to obtain the exergy balance equation for the system and its components. The exergy balance equation for the system and energy and exergy efficiencies for the system are presented below.

Overall system
The exergy balance equation for the overall system can be written as:
$\dot{N}_{1}ex_{1}+\dot{N}_{2}ex_{2}+\dot{N}_{9}ex_{9}-\dot{N}_{air}ex_{air}-\dot{N}_{14}ex_{14}-\dot{N}_{18}ex_{18}-\dot{W}_{\mathrm{net}}-\left(1-\frac{T_{0}}{T_{stack}}\right)(0.2\times\dot{Q}_{stack})\qquad-\left(1-{\frac{T_{0}}{T_{radiator}}}\right){\dot{Q}}_{radiator}-{\dot{I}}_{sysem}=0$
where subscripts 1, 2, 14, and 18 stand for the states of the system shown in Fig. 1. Q̇stack and Q̇radiator are the rate of heat produced by the stack and rate of heat loss by the radiator to the environment, respectively. Also, İsystem is the internal rate of exergy destruction or irreversibility for the overall system. It should be noted that in deriving all exergy balance equations, we assumed the kinetic and potential energies to be negligible and system as well as its components to be at steady state so that time derivatives are zero.
The energy and exergy efficiencies of the system are defined as follows:
$\eta_{system}=\frac{\dot{W}_{net}}{\dot{N}_{1}h_{1}+\dot{N}_{9}h_{9}}$
$\psi_{system}={\frac{\dot{W}_{net}}{\dot{N}_{1}e x_{1}+\dot{N}_{9}e x_{9}}}$


Results:
The analysis presented above is integrated with the fuel cell performance model developed by Baschuk and Li and applied to the system with the fuel cell stack operating at varying temperatures, pressures and air stoichiometric ratios. The base-case operating conditions of the system are listed in Table 2.
The variation of net system and gross stack power with current density at base-case operating conditions is shown in Fig. 2. At a current density of 1.15 A·cm−2 , the net power produced by the system is around 68 kW. It can be observed from the figure that, with the increase of current density in other words, the external load, the difference between the gross stack power and the net system power increases, which is due to the increase in parasitic loads with the increase of external load.

Table 2
Base-case operating conditions
T (◦ C)
P (atm)
Sfuel
Sair
80
3
1.1
2.0

The variation of system energy and exergy efficiencies with current density at base-case operating conditions listed in Table 2 is shown in Fig. 3. The maximum system energy and exergy efficiencies are obtained as 42.32 and 49.59% respectively, at a current density of 0.42 A·cm−2 . The system energy and exergy efficiencies at a typical cell voltage of 0.78 V and current density of 1.15 A·cm−2 are found to be 37.72 and 44.20% respectively. From the figure, it can be seen that both system energy and exergy efficiencies initially increases at lower current densities reaching their peaks and finally decreases with the increase of current density. Since at lower current densities, the molar flow rate of fuel consumed by the stack is less and the power required by the auxiliary devices is low, both energy and exergy efficiencies increases until reaches their threshold values at a current density of 0.42 A·cm−2 and finally decreases with the increase of current density, which is due to the increase in parasitic load and molar consumption of fuel. Exergy efficiencies are higher than energy efficiency, which is due to lower exergy values at states 1 and 9 corresponding to the enthalpy values.
Figs. 4 and 5 show the energy and exergy efficiencies of the system at different operating temperatures of the fuel cell stack. The operating pressure was set as 3 atm, and air and fuel stoichiometries were kept constant at 1.1 and 2.0, respectively. It can be seen that both energy and exergy efficiencies of the system increase with the increase of temperature. This is in fact due to the decrease in irreversible losses (irreversibility) of the fuel cell stack with the increase of temperature, which in turn reduces the irreversibility of the system and hence results in increase of both energy and exergy efficiencies.
Figs. 6 and 7 show the variation of energy and exergy efficiencies of the system with current densities at different operating pressures of the stack. The operating temperature was 80 ◦ C and air and fuel stoichiometries were set as 1.1 and 2.0, respectively. With the increase of pressure, both the energy and exergy efficiencies of the system increases. This is due to significant increase in the gross stack power as a result of decrease in irreversible losses, especially anode and cathode overpotentials, with the increase of pressure.
With the increase of pressure, concentration of the reactants at the reaction sites increases, as a result the irreversible losses in the form of anode and cathode overpotentials decreases, which in turn enhances the performance of the fuel cell stack. Although, high pressure operation requires pressurization of inlet streams, which means more parasitic load in the form of power input to the compressor, but the net power produced by the system increases with the increase of pressure. Therefore, energy and exergy efficiencies of the system increase with the increase of pressure.
The variations of energy and exergy efficiencies of the system at different air stoichiometries are shown in Figs. 8 and 9. The operating temperature and pressure were set as 80 ◦ C and 3 atm with a fuel stoichiometry of 1.1. From the figures, it can be observed there is no appreciable increase in energy and exergy efficiencies with the increase of stoichiometry of air. With the increase of air stoichiometry, molar flow rate of air increases resulting in the decrease of cathode overpotential and hence gross power produced by the stack increases. Although the gross power produced by the stack increases with the increase of air stoichiometry, but the increase in net power produced by system is not significant. Increasing the air stoichiometry from 3.0 to 4.0 has almost no increase in net power produced by the system.
This is again due to increase in parasitic load which is offsetting the increase in gross stack power with air stoichiometry, resulting no significant increase in energy and exergy efficiencies with increase in air stoichiometry. Fig. 10 shows the exergy flow diagram of the system at a particular operating condition. The bold values inside each component of the system denote the irreversibility rate. The system energy and exergy efficiencies are found to be 37.72 and 44.20% respectively. The largest irreversibility rate was found in fuel cell stack. The other major irreversibility rate was found in fuel humidifier, where hydrogen from the storage cylinder and exhaust hydrogen not utilized in the fuel cell stack are mixed and humidified before being fed into the stack. The performance of the system can be enhanced by minimizing the irreversibility rate in the fuel cell stack, which in turn reduces the cost and helps in commercialization of fuel cell power system in transportation applications.