function send_modbus_tcpip(block)

setup(block);
  
%endfunction

%
function setup(block)

  % Register the number of ports.
  block.NumInputPorts  = 1;
  block.NumOutputPorts = 0;

  
  % Set up the port properties to be inherited or dynamic.
  block.SetPreCompPortInfoToDefaults;
  
  % Override the input port properties.
  block.InputPort(1).DatatypeID  = 0;  % double
  block.InputPort(1).Complexity  = 'Real';
  
  % Register the parameters.
  block.NumDialogPrms     = 1;
  block.DialogPrmsTunable = {'Nontunable'};
  %par1   = ssGetNumSFcnParam(block);
  %display(get_Prms(block,0));

  % Register the sample times.
  %  [0 offset]            : Continuous sample time
  %  [positive_num offset] : Discrete sample time
  %
  %  [-1, 0]               : Inherited sample time
  %  [-2, 0]               : Variable sample time
  block.SampleTimes = [-1 0];

  % Specify if Accelerator should use TLC or call back to the 
  % MATLAB file
  block.SetAccelRunOnTLC(false);

  % SetInputPortDimensions:
  block.RegBlockMethod('SetInputPortDimensions', @SetInpPortDims);
  
  % SetInputPortDatatype:
  block.RegBlockMethod('SetInputPortDataType', @SetInpPortDataType);
  
  % PostPropagationSetup:
  block.RegBlockMethod('PostPropagationSetup', @DoPostPropSetup);

  % ProcessParameters  
  block.RegBlockMethod('ProcessParameters', @ProcessPrms);

   
  % InitializeConditions:
  %block.RegBlockMethod('InitializeConditions', @InitializeConditions);
  
  % Start:
  block.RegBlockMethod('Start', @Start);
   
  % Update:
  block.RegBlockMethod('Update', @Update);

function ProcessPrms(block)

  block.AutoUpdateRuntimePrms;
 
%endfunction

function SetInpPortDims(block, idx, di)
  
  block.InputPort(idx).Dimensions = di;

%endfunction
  
function SetInpPortDataType(block, idx, dt)
  
  block.InputPort(idx).DataTypeID = dt;

%endfunction  

function DoPostPropSetup(block)
  block.NumDworks = 1;
  block.Dwork(1).Name            = 'result';
  block.Dwork(1).Dimensions      = 1;
  block.Dwork(1).DatatypeID      = 1;      % single
  block.Dwork(1).Complexity      = 'Real'; % real
  block.Dwork(1).UsedAsDiscState = true;
  
  block.AutoRegRuntimePrms;

  %endfunction


function Start(block)

%read the input parameters
address = '172.20.81.141';
port = 502;
ModBusTCP = modbus('tcpip', address, port);

%ModBusTCP = openConnection(address, port);
%set the variable to hold connection information
set_param(block.BlockHandle, 'UserData', ModBusTCP);
   
%endfunction

function Update(block)
%At every simulation step a new write is made
offset = block.DialogPrm(1).Data+1;
ModBusTCP = get_param(block.BlockHandle, 'UserData');
write(ModBusTCP,'holdingregs',offset,block.InputPort(1).Data,'double');

%endfunction
    


%m = modbus('tcpip', '172.20.81.141', 502);
%write(m,'holdingregs',1,1.001,'double');
%write(m,'holdingregs',9,2.002,'double');
%write(m,'holdingregs',17,3.003,'double');
%write(m,'holdingregs',25,4.004,'double');
%write(m,'holdingregs',33,5.005,'double');
%write(m,'coils',1,1);
%write(m,'coils',1,[1 0 1 0]);
%display (m);

