
function fft_8192_1d_core_config(this_block)

  % Revision History:
  
  %

  this_block.setTopLevelLanguage('VHDL');

  this_block.setEntityName('fft_8192_1d_core_ip_struct');

  % System Generator has to assume that your entity  has a combinational feed through; 
  %   if it  doesn't, then comment out the following line:
  %this_block.tagAsCombinational;

  
  this_block.addSimulinkInport('sync');
  this_block.addSimulinkInport('shift');
  this_block.addSimulinkInport('pol0_in0');
  this_block.addSimulinkInport('pol0_in1');
  this_block.addSimulinkInport('pol0_in2');
  this_block.addSimulinkInport('pol0_in3');
  this_block.addSimulinkInport('pol0_in4');
  this_block.addSimulinkInport('pol0_in5');
  this_block.addSimulinkInport('pol0_in6');
  this_block.addSimulinkInport('pol0_in7');
  this_block.addSimulinkInport('pol0_in8');
  this_block.addSimulinkInport('pol0_in9');
  this_block.addSimulinkInport('pol0_in10');
  this_block.addSimulinkInport('pol0_in11');
  this_block.addSimulinkInport('pol0_in12');
  this_block.addSimulinkInport('pol0_in13');
  this_block.addSimulinkInport('pol0_in14');
  this_block.addSimulinkInport('pol0_in15');
  

  this_block.addSimulinkOutport('sync_out');
  this_block.addSimulinkOutport('out0');
  this_block.addSimulinkOutport('out1');
  this_block.addSimulinkOutport('out2');
  this_block.addSimulinkOutport('out3');
  this_block.addSimulinkOutport('out4');
  this_block.addSimulinkOutport('out5');
  this_block.addSimulinkOutport('out6');
  this_block.addSimulinkOutport('out7');
  this_block.addSimulinkOutport('overflow');

  overflow_port = this_block.port('overflow');
  overflow_port.setType('UFix_4_0');
  out0_port = this_block.port('out0');
  out0_port.setType('UFix_36_0');
  out1_port = this_block.port('out1');
  out1_port.setType('UFix_36_0');
  out2_port = this_block.port('out2');
  out2_port.setType('UFix_36_0');
  out3_port = this_block.port('out3');
  out3_port.setType('UFix_36_0');
  out4_port = this_block.port('out4');
  out4_port.setType('UFix_36_0');
  out5_port = this_block.port('out5');
  out5_port.setType('UFix_36_0');
  out6_port = this_block.port('out6');
  out6_port.setType('UFix_36_0');
  out7_port = this_block.port('out7');
  out7_port.setType('UFix_36_0');
  sync_out_port = this_block.port('sync_out');
  sync_out_port.setType('UFix_1_0');

  % -----------------------------
  if (this_block.inputTypesKnown)
    % do input type checking, dynamic output type and generic setup in this code block.

    if (this_block.port('pol0_in0').width ~= 18);
      this_block.setError('Input data type for port "pol0_in0" must have width=18.');
    end
    if (this_block.port('pol0_in1').width ~= 18);
      this_block.setError('Input data type for port "pol0_in1" must have width=18.');
    end
    if (this_block.port('pol0_in2').width ~= 18);
      this_block.setError('Input data type for port "pol0_in2" must have width=18.');
    end
    if (this_block.port('pol0_in3').width ~= 18);
      this_block.setError('Input data type for port "pol0_in3" must have width=18.');
    end
    if (this_block.port('pol0_in4').width ~= 18);
      this_block.setError('Input data type for port "pol0_in4" must have width=18.');
    end
    if (this_block.port('pol0_in5').width ~= 18);
      this_block.setError('Input data type for port "pol0_in5" must have width=18.');
    end
    if (this_block.port('pol0_in6').width ~= 18);
      this_block.setError('Input data type for port "pol0_in6" must have width=18.');
    end
    if (this_block.port('pol0_in7').width ~= 18);
      this_block.setError('Input data type for port "pol0_in7" must have width=18.');
    end
    if (this_block.port('pol0_in8').width ~= 18);
      this_block.setError('Input data type for port "pol0_in8" must have width=18.');
    end
    if (this_block.port('pol0_in9').width ~= 18);
      this_block.setError('Input data type for port "pol0_in9" must have width=18.');
    end
    if (this_block.port('pol0_in10').width ~= 18);
      this_block.setError('Input data type for port "pol0_in10" must have width=18.');
    end
    if (this_block.port('pol0_in11').width ~= 18);
      this_block.setError('Input data type for port "pol0_in11" must have width=18.');
    end
    if (this_block.port('pol0_in12').width ~= 18);
      this_block.setError('Input data type for port "pol0_in12" must have width=18.');
    end
    if (this_block.port('pol0_in13').width ~= 18);
      this_block.setError('Input data type for port "pol0_in13" must have width=18.');
    end
    if (this_block.port('pol0_in14').width ~= 18);
      this_block.setError('Input data type for port "pol0_in14" must have width=18.');
    end
    if (this_block.port('pol0_in15').width ~= 18);
      this_block.setError('Input data type for port "pol0_in15" must have width=18.');
    end

    if (this_block.port('shift').width ~= 16);
      this_block.setError('Input data type for port "shift" must have width=16.');
    end

    if (this_block.port('sync').width ~= 32);
      this_block.setError('Input data type for port "sync" must have width=32.');
    end

    %this_block.port('sync').useHDLVector(false);

  end  % if(inputTypesKnown)
  % -----------------------------

  % -----------------------------
   if (this_block.inputRatesKnown)
     setup_as_single_rate(this_block,'clk_1','ce_1')
   end  % if(inputRatesKnown)
  % -----------------------------

    % (!) Set the inout port rate to be the same as the first input 
    %     rate. Change the following code if this is untrue.
    uniqueInputRates = unique(this_block.getInputRates);


  % Add addtional source files as needed.
  %  |-------------
  %  | Add files in the order in which they should be compiled.
  %  | If two files "a.vhd" and "b.vhd" contain the entities
  %  | entity_a and entity_b, and entity_a contains a
  %  | component of type entity_b, the correct sequence of
  %  | addFile() calls would be:
  %  |    this_block.addFile('b.vhd');
  %  |    this_block.addFile('a.vhd');
  %  |-------------

  %    this_block.addFile('');
  %    this_block.addFile('');
  %this_block.addFile('fft_2048ch_6a_core/sysgen/fft_2048ch_6a_core.vhd');
  this_block.addFile('fft_8192_1d_core.vhd');

return;


% ------------------------------------------------------------

function setup_as_single_rate(block,clkname,cename) 
  inputRates = block.inputRates; 
  uniqueInputRates = unique(inputRates); 
  if (length(uniqueInputRates)==1 & uniqueInputRates(1)==Inf) 
    block.addError('The inputs to this block cannot all be constant.'); 
    return; 
  end 
  if (uniqueInputRates(end) == Inf) 
     hasConstantInput = true; 
     uniqueInputRates = uniqueInputRates(1:end-1); 
  end 
  if (length(uniqueInputRates) ~= 1) 
    block.addError('The inputs to this block must run at a single rate.'); 
    return; 
  end 
  theInputRate = uniqueInputRates(1); 
  for i = 1:block.numSimulinkOutports 
     block.outport(i).setRate(theInputRate); 
  end 
  block.addClkCEPair(clkname,cename,theInputRate); 
  return; 

% ------------------------------------------------------------

