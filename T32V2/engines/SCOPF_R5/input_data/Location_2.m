function mpc = Location_2
%LOCATION_2
%   PSS(R)E 33 RAW created by rawd33  THU, DEC 03 2020  10:14
%   CREATED BY NETVISION RAW CONVERTER FROM FILES: NDC_2019-11-1
%   , BEGIN BUS DATA
%
%   Converted by MATPOWER 7.0 using PSSE2MPC on 03-Dec-2020
%   from 'Location 2.raw' using PSS/E rev 33 format.
%
%   WARNINGS:
%       Conversion explicitly using PSS/E revision 33
%       Skipped 2 lines of zone data.
%
%   See CASEFORMAT for details on the MATPOWER case file format.

%% MATPOWER Case Format : Version 2
mpc.version = '2';

%%-----  Power Flow Data  -----%%
%% system MVA base
mpc.baseMVA = 100;

%% bus data
%	bus_i	type	Pd	Qd	Gs	Bs	area	Vm	Va	baseKV	zone	Vmax	Vmin
mpc.bus = [
	1	3	145.168	31.357	6.728	9.39	8	1.026	0	400	1	1.1	0.9;
	2	1	487.748	114.827	0.001	18.845	8	1.01791	-1.9356	400	1	1.1	0.9;
	3	1	-184.75	93.595	9.456	-14.92	8	1.02459	0.2666	400	1	1.1	0.9;
	4	2	-216.617	0	0	66.844	8	1.03931	6.6407	400	1	1.1	0.9;
	5	1	-50.122	-3.328	-5.577	42.668	8	1.10181	8.3207	220	1	1.1	0.9;
	6	1	103.854	12.948	0	1.099	8	1.0719	-3.1739	220	1	1.1	0.9;
	7	1	23.196	0	0	94.889	8	1.08167	1.7659	220	1	1.1	0.9;
	8	2	0	0	0	0	8	1.101	9.2934	220	1	1.1	0.9;
	9	1	3.924	45.55	0.001	5.586	8	1.07526	0.8916	220	1	1.1	0.9;
	10	1	11.273	-1.88	0	0	8	1.05083	-0.2407	110	1	1.1	0.9;
	11	1	7.652	-2.369	0	0	8	1.05975	-2.6498	110	1	1.1	0.9;
	12	1	4.861	2.959	0	1.336	8	1.06712	5.2158	110	1	1.1	0.9;
	13	2	10.12	-1.565	0	0	8	1.04355	-1.2749	110	1	1.1	0.9;
	14	1	0.687	-0.335	0	0	8	1.07152	1.7885	110	1	1.1	0.9;
	15	1	14.534	-10.987	0	0	8	1.05376	-3.1103	110	1	1.1	0.9;
	16	1	6.963	-5.925	0	0	8	1.06724	-4.401	110	1	1.1	0.9;
	17	1	67.365	-3.702	4.992	-28.965	8	1.03164	-2.6541	110	1	1.1	0.9;
	18	1	34.249	2.589	-0.471	1.423	8	1.05941	2.9759	110	1	1.1	0.9;
	19	1	3.446	-3.143	0	0	8	1.07173	0.9722	110	1	1.1	0.9;
	20	2	-46.158	3.658	-1.198	0.317	8	1.0672	6.1453	110	1	1.1	0.9;
	21	1	6.609	0.871	0	0	8	1.07607	3.5994	110	1	1.1	0.9;
	22	2	3.316	-0.092	0	0	8	1.06757	1.6398	110	1	1.1	0.9;
	23	1	5.309	-1.563	0	0	8	1.07167	-0.8772	110	1	1.1	0.9;
	24	1	0	0	0	0	8	1.06594	6.2959	110	1	1.1	0.9;
	25	2	0	0	0	0	8	1.07618	3.3885	110	1	1.1	0.9;
	26	2	2.912	-0.511	0	0	8	1.08464	4.3195	110	1	1.1	0.9;
	27	2	20.33	5.262	0	0	8	1.07036	3.2779	110	1	1.1	0.9;
	28	1	4.743	-2.337	0	0	8	1.03631	-2.1788	110	1	1.1	0.9;
	29	1	11.405	-7.702	-2.56	20.418	8	1.04795	-1.3012	110	1	1.1	0.9;
];

%% generator data
%	bus	Pg	Qg	Qmax	Qmin	Vg	mBase	status	Pmax	Pmin	Pc1	Pc2	Qc1min	Qc1max	Qc2min	Qc2max	ramp_agc	ramp_10	ramp_30	ramp_q	apf
mpc.gen = [
	1	0	0.071	9999	-9999	1.026	100	1	9999	-9999	0	0	0	0	0	0	0	0	0	0	0;
	4	103.286	-61.334	80	-80	1.03931	155	1	138	-130	0	0	0	0	0	0	0	0	0	0	0;
	4	105.462	-62.626	80	-80	1.03931	155	1	138	-130	0	0	0	0	0	0	0	0	0	0	0;
	8	67.907	-6.318	35	-30.88	1.101	80	1	72	35	0	0	0	0	0	0	0	0	0	0	0;
	13	16.712	-5.837	29.75	-15	1.04355	35	1	31.5	0.01	0	0	0	0	0	0	0	0	0	0	0;
	13	16.617	-5.804	29.75	-15	1.04355	35	1	31.5	0.01	0	0	0	0	0	0	0	0	0	0	0;
	13	0	0	29.75	-15	1.04355	35	0	31.5	0.01	0	0	0	0	0	0	0	0	0	0	0;
	20	1.218	3.863	4.85	-4.85	1.0672	11.12	1	10	0.01	0	0	0	0	0	0	0	0	0	0	0;
	22	2.989	-0.212	1.87	-1.87	1.06757	6	1	6	0.01	0	0	0	0	0	0	0	0	0	0	0;
	25	40.905	0.855	13.11	-13.11	1.07618	45	1	42	0.01	0	0	0	0	0	0	0	0	0	0	0;
	26	69.65	-7.32	35	-45	1.08464	80	1	72	35	0	0	0	0	0	0	0	0	0	0	0;
	26	69.52	-7.306	35	-45	1.08464	80	1	72	35	0	0	0	0	0	0	0	0	0	0	0;
	27	18.315	0.878	17.25	-7.8	1.07036	25	1	24	0.01	0	0	0	0	0	0	0	0	0	0	0;
];

%% branch data
%	fbus	tbus	r	x	b	rateA	rateB	rateC	ratio	angle	status	angmin	angmax
mpc.branch = [
	1	3	0.00114375	0.011895	0.3377	1330	0	0	0	0	1	-360	360;
	1	3	0.0310033	0.171211	0	0	0	0	0	0	1	-360	360;
	1	7	0.011412	0.119894	0	0	0	0	0	0	1	-360	360;
	1	29	0.698874	1.5351	0	0	0	0	0	0	1	-360	360;
	2	3	0.00239125	0.0263025	0.718	1330	0	0	0	0	1	-360	360;
	2	4	0.00367188	0.0381762	1.00701	1330	0	0	0	0	1	-360	360;
	3	7	0.0134423	0.125263	0	0	0	0	0	0	1	-360	360;
	3	29	0.0757434	0.345646	0	0	0	0	0	0	1	-360	360;
	4	5	0.0315312	0.230399	0	0	0	0	0	0	1	-360	360;
	4	18	0.150636	0.630573	0	0	0	0	0	0	1	-360	360;
	4	20	0.13981	0.468878	0	0	0	0	0	0	1	-360	360;
	5	7	0.0146033	0.0778843	0.20069	366	0	0	0	0	1	-360	360;
	5	8	0.00256198	0.0137603	0.02014	310	0	0	0	0	1	-360	360;
	5	18	1.14749	2.99257	0	0	0	0	0	0	1	-360	360;
	5	20	0.98949	2.20715	0	0	0	0	0	0	1	-360	360;
	6	8	0.00913223	0.0489463	0.07139	310	0	0	0	0	0	-360	360;
	6	17	0.0230585	0.119891	0	0	0	0	0	0	1	-360	360;
	7	9	0.00436364	0.0223636	0.03552	311	0	0	0	0	1	-360	360;
	7	29	0.498523	1.25207	0	0	0	0	0	0	1	-360	360;
	10	13	0.0085124	0.0270248	0.00262	123	0	0	0	0	1	-360	360;
	10	15	0.0194223	0.0451083	0.03175	70	0	0	0	0	0	-360	360;
	10	25	0.0254545	0.0838843	0.00848	123	0	0	0	0	1	-360	360;
	11	15	0.0112397	0.0387603	0.00867	123	0	0	0	0	1	-360	360;
	11	23	0.0359496	0.105209	0.10799	100	0	0	0	0	1	-360	360;
	12	20	0.021157	0.0721488	0.00701	123	0	0	0	0	1	-360	360;
	12	27	0.0544628	0.186364	0.01877	123	0	0	0	0	1	-360	360;
	13	17	0.0140496	0.0470248	0.00467	123	0	0	0	0	1	-360	360;
	13	28	0.0121488	0.0408347	0.00407	123	0	0	0	0	1	-360	360;
	13	29	0.0134711	0.0438017	0.0042	82	0	0	0	0	1	-360	360;
	13	29	0.0119835	0.0405785	0.00413	135	0	0	0	0	1	-360	360;
	14	19	0.0199198	0.0685124	0.00687	100	0	0	0	0	1	-360	360;
	14	27	0.0347107	0.119339	0.01196	123	0	0	0	0	1	-360	360;
	15	16	0.103226	0.2081	0.08041	70	0	0	0	0	1	-360	360;
	15	17	0.0301653	0.0601653	0.03386	100	0	0	0	0	1	-360	360;
	17	28	0.00760331	0.0245454	0.00314	123	0	0	0	0	1	-360	360;
	18	20	0.0447273	0.152818	0.01473	123	0	0	0	0	1	-360	360;
	18	20	0.982326	1.40753	0	0	0	0	0	0	1	-360	360;
	18	22	0.0299967	0.10165	0.00971	100	0	0	0	0	1	-360	360;
	19	22	0.0153719	0.052562	0.00508	114	0	0	0	0	1	-360	360;
	19	23	0.0269232	0.0859798	0.10829	100	0	0	0	0	1	-360	360;
	20	24	0.00231405	0.0181818	0.00292	311	0	0	0	0	1	-360	360;
	21	26	0.0531421	0.120579	0.01126	90	0	0	0	0	1	-360	360;
	21	27	0.0533058	0.120496	0.01123	90	0	0	0	0	1	-360	360;
	25	26	0.0128099	0.0422314	0.00422	123	0	0	0	0	1	-360	360;
	1	9	0.00036456	0.0317479	0	400	0	0	0.947619048	0.46	1	-360	360;
	2	6	0.00036694	0.0290227	0	400	0	0	0.952380952	0	1	-360	360;
	2	6	0.00038825	0.0297475	0	400	0	0	0.952380952	0	0	-360	360;
	4	24	0.00057011	0.0404627	0	300	0	0	0.978521739	0	1	-360	360;
	6	17	0.00182489	0.0741109	0	150	0	0	1.06365217	0	1	-360	360;
	6	17	0.00173556	0.0706453	0	150	0	0	1.06365217	0	1	-360	360;
	8	26	0.00068375	0.0651964	0	200	0	0	1.00057394	7.58	1	-360	360;
];

%% bus names
mpc.bus_name = {
	'BUS1        ';
	'BUS2        ';
	'BUS3        ';
	'BUS4        ';
	'BUS5        ';
	'BUS6        ';
	'BUS7        ';
	'BUS8        ';
	'BUS9        ';
	'BUS10       ';
	'BUS11       ';
	'BUS12       ';
	'BUS13       ';
	'BUS14       ';
	'BUS15       ';
	'BUS16       ';
	'BUS17       ';
	'BUS18       ';
	'BUS19       ';
	'BUS20       ';
	'BUS21       ';
	'BUS22       ';
	'BUS23       ';
	'BUS24       ';
	'BUS25       ';
	'BUS26       ';
	'BUS27       ';
	'BUS28       ';
	'BUS29       ';
};