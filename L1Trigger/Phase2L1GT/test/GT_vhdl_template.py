




def portdefaults():
		print("""
port map (
clk           => clk, -- ipbus signals
rst           => rst,
ipb_in        => ipb_in,
ipb_out       => open,
clk_algo => clk_algo,
rst_algo => rst_algo,
objects_valid => delayed_valid(BX_ZERO),""")

def writeVHDLintro():
		print("""
--- Algo template Generated from gt-algorithm: p2gt_algos.vhdl
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.all;

use work.ipbus.all;
use work.emp_data_types.all;
use work.emp_project_decl.all;

use work.emp_device_decl.all;
use work.emp_ttc_decl.all;

use work.common_pkg.all;

entity p2gt_algos is
  generic (
    cut_offset                                 : natural := 0
  );
  port (
    clk                                        : in std_logic; -- ipbus signals
    rst                                        : in std_logic;
    ipb_in                                     : in ipb_wbus;
    ipb_out                                    : out ipb_rbus;
    clk_algo                                   : in std_logic;
    rst_algo                                   : in std_logic;
    clk40                                      : in std_logic;
    rst40                                      : in std_logic;
    objects_valid                              : in std_logic;
    objects                                    : in t_obj_array(NUM_OBJ_TYPES-1 downto 0);
    algo_bits_valid_out                        : out std_logic;
    algo_bits_out                              : out std_logic_vector(NUM_ALGOS_IN_SRL-1 downto 0)
  );

end p2gt_algos;

architecture rtl of p2gt_algos is
  signal algo_bits_int, algo_bits_int2         : std_logic_vector(NUM_ALGOS_IN_SRL-1 downto 0);
  signal algo_bits_srl1_int                    : std_logic_vector(NUM_ALGOS_IN_SRL-1 downto 0);
  signal algo_bits_srl2_int                    : std_logic_vector(NUM_ALGOS_IN_SRL-1 downto 0);

  signal delayed_valid_to_payload : std_logic_vector(ALGO_REPLICATION_IN_SRL-1 downto 0);
  signal delayed_valid_buffer     : std_logic_vector(ALGO_LATENCY-1 downto 0);  -- TODO: 1 tick used for registering algo bits.""")



def writeVHDLintermediatefirst():
	print("""



begin
  ipb_out <= IPB_RBUS_NULL;

  delayed_valid_buffer(0) <= delayed_valid_to_payload(0);

  process(clk_algo)
  begin
    if rising_edge(clk_algo) then
      delayed_valid_buffer(delayed_valid_buffer'high downto 1) <= delayed_valid_buffer(delayed_valid_buffer'high-1 downto 0);
    end if;
  end process;





  algos : for i in 0 to ALGO_REPLICATION_IN_SRL-1 generate
    signal delayed_objects_tmp : t_delayed_obj_array(0 to 4);
    signal delayed_objects     : t_delayed_obj_array(0 to 4);
    signal delayed_valid_tmp   : std_logic_vector(0 to 4);
    signal delayed_valid       : std_logic_vector(0 to 4);

    ATTRIBUTE max_fanout                    : integer;
    ATTRIBUTE max_fanout of delayed_objects : signal is 10;
    ATTRIBUTE max_fanout of delayed_valid   : signal is 10;
  begin 
    object_delay : entity work.p2gt_objectDelay
    port map (
      clk_algo        => clk_algo,
      rst_algo        => rst_algo,
      objects_valid   => objects_valid,
      objects         => objects,
      delayed_objects => delayed_objects_tmp,
      delayed_valid   => delayed_valid_tmp
    );



    reg_objects : process(clk_algo)
    begin
      if rising_edge(clk_algo) then
        delayed_objects <= delayed_objects_tmp;
        delayed_valid   <= delayed_valid_tmp;
      end if;
    end process reg_objects;

  delayed_valid_to_payload(i) <= delayed_valid(BX_ZERO);


""")

def writeVHDLintermediatesecond():
	print("""
  end generate;

  reg_outputs : process(clk_algo)  -- Register on algo clk for one BX
  begin
    if rising_edge(clk_algo) then """)


def WriteVHDLend():
	print("""
        algo_bits_out <= algo_bits_int2;
    end if;
  end process;
  algo_bits_valid_out <= delayed_valid_buffer(delayed_valid_buffer'high);

end rtl;""")
