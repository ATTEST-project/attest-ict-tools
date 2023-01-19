% Simplified UK transmission network
% References
% https://ieeexplore-ieee-org.manchester.idm.oclc.org/document/5589807
function mpc = Transmission_Network_UK_2020()


%% MATPOWER Case Format : Version 2
mpc.version = '2';

%%-----  Power Flow Data  -----%%
%% system MVA base
mpc.baseMVA = 100;

%% bus data													
%	bus_i	type	Pd	Qd	Gs	Bs	area	Vm	Va	baseKV	zone	Vmax	Vmin
mpc.bus = [													
1	2	468	102	0	0	1	1	0	275	1	1.05	0.95;
2	2	513	113	0	0	1	1	0	275	1	1.05	0.95;
3	2	555	105	0	0	1	1	0	132	1	1.05	0.95;
4	2	1308	317	0	0	1	1	0	275	1	1.05	0.95;
5	2	502	128	0	0	1	1	0	400	1	1.05	0.95;
6	2	1176	315	0	0	1	1	0	400	1	1.05	0.95;
7	2	745	171	0	0	1	1	0	400	1	1.05	0.95;
8	2	1000	37.4	0	0	1	1	0	400	1	1.05	0.95;
9	2	130	53	0	0	1	1	0	400	1	1.05	0.95;
10	2	2561	465	0	0	1	1	0	400	1	1.05	0.95;
11	2	3360	760	0	0	1	1	0	400	1	1.05	0.95;
12	2	1189	338	0	0	1	1	0	400	1	1.05	0.95;
13	2	2524	766	0	0	1	1	0	400	1	1.05	0.95;
14	2	1831	566.5	0	0	1	1	0	400	1	1.05	0.95;
15	2	2633	694.6	0	0	1	1	0	400	1	1.05	0.95;
16	2	1607	655	0	0	1	1	0	400	1	1.05	0.95;
17	2	1081	371	0	0	1	1	0	400	1	1.05	0.95;
18	2	5362	1935	0	0	1	1	0	400	1	1.05	0.95;
19	2	2019	648	0	0	1	1	0	400	1	1.05	0.95;
20	2	1027.36	305.8	0	0	1	1	0	400	1	1.05	0.95;
21	2	702	202.2	0	0	1	1	0	400	1	1.05	0.95;
22	2	1820	665	0	0	1	1	0	400	1	1.05	0.95;
23	2	4734	1337	0	0	1	1	0	400	1	1.05	0.95;
24	2	1418	528	0	0	1	1	0	400	1	1.05	0.95;
25	2	9734	2902	0	0	1	1	0	400	1	1.05	0.95;
26	2	1424	434	0	0	1	1	0	400	1	1.05	0.95;
27	3	457	138	0	0	1	1	0	400	1	1.05	0.95;
28	2	2751	841	0	0	1	1	0	400	1	1.05	0.95;
29	2	2577	356	0	0	1	1	0	400	1	1.05	0.95;
30  2	0	0	0	0	1	1	0	275	1	1.05	0.95;
];													

%% branch data														
%	fbus	tbus	r	x	b	rateA	rateB	rateC	tap ratio	shift angle	status	angmin	angmax	%name
mpc.branch = [														
1	2	0.0122	0.02	0.0856	525	0	0	0	0	1	-360	360;
1	2	0.0122	0.02	0.2844	525	0	0	0	0	1	-360	360;
1	3	0.007	0.15	0.052	132	0	0	0	2	1	-360	360;
1	3	0.007	0.15	0.052	132	0	0	0	2	1	-360	360;
2	4	0.0004	0.065	0.4454	760	0	0	0	0	1	-360	360;
2	4	0.0004	0.065	0.5545	760	0	0	0	0	1	-360	360;
4	6	0.0013	0.023	0.1496	1500	0	0	0	0	1	-360	360;
4	6	0.0013	0.023	0.1758	1120	0	0	0	0	1	-360	360;
4	5	0.001	0.024	0.125	1000	0	0	0	0	1	-360	360;
4	5	0.001	0.024	0.125	1000	0	0	0	0	1	-360	360;
4	7	0.0021	0.0135	0.1538	1090	0	0	0	0	1	-360	360;
4	7	0.00211	0.0135	0.1174	1090	0	0	0	0	1	-360	360;
5	6	0.00085	0.01051	0.38254	1390	0	0	0	0	1	-360	360;
5	6	0.00151	0.01613	0.59296	1390	0	0	0	0	1	-360	360;
6	9	0.00078	0.00852	0.0737	2100	0	0	0	0	1	-360	360;
6	9	0.00078	0.00852	0.4635	2100	0	0	0	0	1	-360	360;
7	8	0.0004	0.0001	0.728	2180	0	0	0	0	1	-360	360;
7	8	0.0004	0.0001	1.2872	2500	0	0	0	0	1	-360	360;
7	6	0.003	0.2	0.2939	950	0	0	0	0	1	-360	360;
7	6	0.003	0.2	0.2939	950	0	0	0	0	1	-360	360;
8	10	0.00083	0.0175	0.6624	3070	0	0	0	0	1	-360	360;
8	10	0.00083	0.0175	0.6624	3070	0	0	0	0	1	-360	360;
9	11	0.00164	0.0163	0.4868	1390	0	0	0	0	1	-360	360;
9	11	0.00164	0.0163	0.4868	1390	0	0	0	0	1	-360	360;
9	10	0.00352	0.02453	0.1898	855	0	0	0	0	1	-360	360;
9	10	0.00492	0.0343	0.2502	775	0	0	0	0	1	-360	360;
10	15	0.00053	0.00835	5.373	4840	0	0	0	0	1	-360	360;
10	15	0.00052	0.0063	1.0636	4020	0	0	0	0	1	-360	360;
11	15	0.0007	0.042	0.3907	2520	0	0	0	0	1	-360	360;
11	15	0.00099	0.042	0.5738	2520	0	0	0	0	1	-360	360;
11	13	0.0004	0.0052	0.2498	2170	0	0	0	0	1	-360	360;
11	13	0.0004	0.0052	0.2664	2210	0	0	0	0	1	-360	360;
11	12	0.0001	0.0085	0.0798	3320	0	0	0	0	1	-360	360;
11	12	0.0001	0.0085	0.0798	3320	0	0	0	0	1	-360	360;
12	13	0.00096	0.01078	0.385	3100	0	0	0	0	1	-360	360;
12	18	0.00074	0.009	0.2911	2400	0	0	0	2	1	-360	360;
12	18	0.00097	0.009	0.3835	2400	0	0	0	2	1	-360	360;
12	13	0.00096	0.01078	0.385	3100	0	0	0	0	1	-360	360;
13	18	0.00049	0.007	0.1943	2400	0	0	0	0	1	-360	360;
13	18	0.00084	0.007	0.7759	2400	0	0	0	0	1	-360	360;
13	15	0.00137	0.023	0.6643	1240	0	0	0	0	1	-360	360;
13	15	0.00164	0.023	0.1104	955	0	0	0	0	1	-360	360;
13	14	0.00107	0.01163	1.1745	1040	0	0	0	0	1	-360	360;
13	14	0.00082	0.01201	1.2125	1040	0	0	0	0	1	-360	360;
14	16	0.0005	0.016	0.2795	2580	0	0	0	0	1	-360	360;
14	16	0.005	0.018	0.1466	625	0	0	0	0	1	-360	360;
15	16	0.00033	0.0052	0.3534	2770	0	0	0	0	1	-360	360;
15	16	0.00016	0.00172	0.3992	5540	0	0	0	0	1	-360	360;
15	14	0.00019	0.00222	0.7592	5000	0	0	0	0	1	-360	360;
15	14	0.00018	0.00222	0.5573	5000	0	0	0	0	1	-360	360;
16	19	0.00056	0.0141	0.4496	2780	0	0	0	0	1	-360	360;
16	19	0.00056	0.0141	0.4496	3820	0	0	0	0	1	-360	360;
17	16	0.001	0.01072	0.2651	2150	0	0	0	0	1	-360	360;
17	16	0.001	0.01072	0.4573	1890	0	0	0	0	1	-360	360;
17	22	0.00068	0.0097	0.4566	2100	0	0	0	0	1	-360	360;
17	22	0.00069	0.0097	0.4574	2100	0	0	0	0	1	-360	360;
18	17	0.00042	0.0018	0.2349	3100	0	0	0	0	1	-360	360;
18	17	0.00042	0.0018	0.2349	3460	0	0	0	0	1	-360	360;
18	23	0.00138	0.0096	0.4829	1970	0	0	0	0	1	-360	360;
18	23	0.00117	0.0096	0.4122	1970	0	0	0	0	1	-360	360;
20	26	0.00035	0.0023	0.2249	2780	0	0	0	0	1	-360	360;
20	26	0.00035	0.0023	0.2249	2780	0	0	0	0	1	-360	360;
20	19	0.00178	0.0213	0.6682	1590	0	0	0	0	1	-360	360;
20	19	0.00132	0.0143	0.3656	1590	0	0	0	0	1	-360	360;
21	16	0.00145	0.01824	0.9169	2780	0	0	0	0	1	-360	360;
21	16	0.00145	0.01824	0.9169	2780	0	0	0	0	1	-360	360;
21	25	0.00025	0.01	0.1586	2780	0	0	0	0	1	-360	360;
21	25	0.00025	0.01	0.1586	2780	0	0	0	0	1	-360	360;
21	20	0.0012	0.0048	0.4446	2780	0	0	0	0	1	-360	360;
21	20	0.0012	0.0048	0.7	2780	0	0	0	0	1	-360	360;
21	19	0.00037	0.0059	0.294	3030	0	0	0	0	1	-360	360;
21	19	0.00037	0.0059	0.2955	2780	0	0	0	0	1	-360	360;
22	16	0.00178	0.0172	0.8403	2010	0	0	0	0	1	-360	360;
22	16	0.00178	0.0172	0.627	2010	0	0	0	0	1	-360	360;
22	25	0.00037	0.0041	0.4098	3275	0	0	0	0	1	-360	360;
22	25	0.00034	0.0041	0.429	3275	0	0	0	0	1	-360	360;
22	21	0.00019	0.00111	0.1232	2780	0	0	0	0	1	-360	360;
22	21	0.00048	0.0061	0.3041	2780	0	0	0	0	1	-360	360;
23	29	0.00151	0.0182	0.53	2010	0	0	0	0	1	-360	360;
23	24	0.00086	0.0008	0.9622	2780	0	0	0	0	1	-360	360;
23	24	0.00023	0.0007	2.8447	4400	0	0	0	0	1	-360	360;
23	22	0.00055	0.003	0.3468	2780	0	0	0	0	1	-360	360;
23	22	0.00039	0.003	0.2466	2770	0	0	0	0	1	-360	360;
23	29	0.00151	0.0182	0.53	2010	0	0	0	0	1	-360	360;
24	28	0.00068	0.007	0.2388	2210	0	0	0	0	1	-360	360;
24	25	0.00104	0.0091	0.2918	1390	0	0	0	0	1	-360	360;
24	25	0.00104	0.0091	0.2918	1390	0	0	0	0	1	-360	360;
24	28	0.00068	0.007	0.2388	2210	0	0	0	0	1	-360	360;
25	26	0.0002	0.0057	0.532	6960	0	0	0	0	1	-360	360;
25	26	0.0002	0.0057	0.532	5540	0	0	0	0	1	-360	360;
27	26	0.0002	0.00503	0.1797	3100	0	0	0	0	1	-360	360;
27	26	0.0002	0.00503	0.1797	3100	0	0	0	0	1	-360	360;
28	27	0.00038	0.00711	0.2998	3070	0	0	0	0	1	-360	360;
28	27	0.00038	0.00711	0.2998	3070	0	0	0	0	1	-360	360;
29	28	0.00051	0.00796	0.34	2780	0	0	0	0	1	-360	360;
29	28	0.00051	0.00796	0.34	2780	0	0	0	0	1	-360	360;
3	4	0.003	0.041	0.0044	648	0	0	0	0	1	-360	360;
3	4	0.003	0.041	0.044	648	0	0	0	0	1	-360	360;
3	2	0.03004	0.077	0.0124	652	0	0	0	0	1	-360	360;
1	30	0.03004	0.077	0.0124	652	0	0	0	0	1	-360	360;
];				
%% generator data																						
%	bus	Pg	Qg	Qmax	Qmin	Vg	mBase	status	Pmax	Pmin	Pc1	Pc2	Qc1min	Qc1max	Qc2min	Qc2max	ramp_agc	ramp_10	ramp_30	ramp_q	apf	
mpc.gen = [																						
1	396.774	-49.18	139.2209046	-188.4590954	1	100	1	493.5	0	0	0	0	0	0	0	0	0	0	0	0	;
1	441.86232	0	105.2292729	-66.29666644	1	100	1	549.58	0	0	0	0	0	0	0	0	0	0	0	0	;
1	0	0	180	-100	1	100	1	0	0	0	0	0	0	0	0	0	0	0	0	0	;
1	15.05088	0	7.8	-8.99	1	100	1	18.72	0	0	0	0	0	0	0	0	0	0	0	0	;
2	29.28972	0	14.328265	-17.671735	1	100	1	36.43	0	0	0	0	0	0	0	0	0	0	0	0	;
2	1225.296	267.04	1108.510424	-473.3565078	1	100	1	1524	0	0	0	0	0	0	0	0	0	0	0	0	;
2	9.648	0	0	0	1	100	1	12	0	0	0	0	0	0	0	0	0	0	0	0	;
3	311.8716	128.3364	128.3364217	-158.1387783	1	100	1	387.9	0	0	0	0	0	0	0	0	0	0	0	0	;
3	10.88616	0	-3.51124	-3.51124	1	100	1	13.54	0	0	0	0	0	0	0	0	0	0	0	0	;
3	444.612	124.3	144.7939487	-66.16987334	1	100	1	553	0	0	0	0	0	0	0	0	0	0	0	0	;
3	12.15648	0	6.5071	-7.2929	1	100	1	15.12	0	0	0	0	0	0	0	0	0	0	0	0	;
4	20.2608	0	10.65561979	-12.34438021	1	100	1	25.2	0	0	0	0	0	0	0	0	0	0	0	0	;
4	1836.336	597.14	641.4683118	-679.0037586	1	100	1	2284	0	0	0	0	0	0	0	0	0	0	0	0	;
4	273.36	0	150.34	-137.8599087	1	100	1	340	0	0	0	0	0	0	0	0	0	0	0	0	;
4	208.236	0	137.27	-122.95	1	100	1	259	0	0	0	0	0	0	0	0	0	0	0	0	;
5	863.496	-28.9	416.4725632	-429.7731578	1	100	1	1074	0	0	0	0	0	0	0	0	0	0	0	0	;
5	18.6528	0	15.38765205	-9.937777586	1	100	1	23.2	0	0	0	0	0	0	0	0	0	0	0	0	;
6	805.22208	244.84	439.66182	-484.8030489	1	100	1	1001.52	0	0	0	0	0	0	0	0	0	0	0	0	;
6	26.532	0	24.8	-25.5	1	100	1	33	0	0	0	0	0	0	0	0	0	0	0	0	;
6	39.7176	0	12.0901377	-17.4898623	1	100	1	49.4	0	0	0	0	0	0	0	0	0	0	0	0	;
7	182.3472	-111.07	125.7559808	-131.0176558	1	100	1	226.8	0	0	0	0	0	0	0	0	0	0	0	0	;
7	977.664	0	681.3407231	-469.0728269	1	100	1	1216	0	0	0	0	0	0	0	0	0	0	0	0	;
7	887.616	0	220.3438921	-205.2405431	1	100	1	1104	0	0	0	0	0	0	0	0	0	0	0	0	;
10	971.232	233.67	559.1941175	-539.6840776	1	100	1	1208	0	0	0	0	0	0	0	0	0	0	0	0	;
10	1507.5	0	697.1712682	-829.6266854	1	100	1	1875	0	0	0	0	0	0	0	0	0	0	0	0	;
10	337.68	0	167.9526233	-138.0443168	1	100	1	420	0	0	0	0	0	0	0	0	0	0	0	0	;
11	104.77728	0	-57.6	-57.6	1	100	1	130.32	0	0	0	0	0	0	0	0	0	0	0	0	;
11	1934.424	1189.27	1216.095081	-1006.32167	1	100	1	2406	0	0	0	0	0	0	0	0	0	0	0	0	;
11	1576.644	0	873.2160163	-571.4617135	1	100	1	1961	0	0	0	0	0	0	0	0	0	0	0	0	;
11	124.62	0	94.22483304	-75.20860942	1	100	1	155	0	0	0	0	0	0	0	0	0	0	0	0	;
11	835.356	0	670.3158949	-539.0705317	1	100	1	1039	0	0	0	0	0	0	0	0	0	0	0	0	;
12	787.92	357.62	579.9839977	-418.117905	1	100	1	980	0	0	0	0	0	0	0	0	0	0	0	0	;
12	1515.54	0	960.0493991	-853.0598839	1	100	1	1885	0	0	0	0	0	0	0	0	0	0	0	0	;
12	168.84	0	116.4182172	-94.96519991	1	100	1	210	0	0	0	0	0	0	0	0	0	0	0	0	;
12	881.184	0	344.4771874	-575.5228126	1	100	1	1096	0	0	0	0	0	0	0	0	0	0	0	0	;
15	6271.2	1243.37	3535.031883	-2527.871669	1	100	1	7800	0	0	0	0	0	0	0	0	0	0	0	0	;
16	3193.488	0	1587.056017	-1289.624064	1	100	1	3972	0	0	0	0	0	0	0	0	0	0	0	0	;
16	5660.964	3118.9	3653.234202	-3354.578181	1	100	1	7041	0	0	0	0	0	0	0	0	0	0	0	0	;
16	979.272	0	767.3265276	-562.8491075	1	100	1	1218	0	0	0	0	0	0	0	0	0	0	0	0	;
17	1608	356.18	814.2321995	-405.9415934	1	100	1	2000	0	0	0	0	0	0	0	0	0	0	0	0	;
18	1575.84	-45.33	884.9714977	-534.171232	1	100	1	1960	0	0	0	0	0	0	0	0	0	0	0	0	;
18	183.312	0	40.02176281	-73.57823719	1	100	1	228	0	0	0	0	0	0	0	0	0	0	0	0	;
19	2287.38	1201.13	1336.631772	-1468.981903	1	100	1	2845	0	0	0	0	0	0	0	0	0	0	0	0	;
19	327.0672	0	162.7	-162.7	1	100	1	406.8	0	0	0	0	0	0	0	0	0	0	0	0	;
20	964.8	304.42	621.1413306	-523.3801299	1	100	1	1200	0	0	0	0	0	0	0	0	0	0	0	0	;
20	289.44	0	236.64	236.64	1	100	1	360	0	0	0	0	0	0	0	0	0	0	0	0	;
21	534.66	326	326.1499173	-306.0698826	1	100	1	665	0	0	0	0	0	0	0	0	0	0	0	0	;
22	322.4844	130.03	189.7190044	-232.6810031	1	100	1	401.1	0	0	0	0	0	0	0	0	0	0	0	0	;
23	3032.688	1254.4	1589.66533	-1388.267098	1	100	1	3772	0	0	0	0	0	0	0	0	0	0	0	0	;
23	291.852	0	84.80580067	-153.9941993	1	100	1	363	0	0	0	0	0	0	0	0	0	0	0	0	;
23	377.88	0	317.7576473	-211.4291086	1	100	1	470	0	0	0	0	0	0	0	0	0	0	0	0	;
23	2477.13204	0	1200.813571	-1262.242187	1	100	1	3081.01	0	0	0	0	0	0	0	0	0	0	0	0	;
25	1706.892	941	949.3783757	-947.4163172	1	100	1	2123	0	0	0	0	0	0	0	0	0	0	0	0	;
25	0	0	0	0	1	100	1	100	0	0	0	0	0	0	0	0	0	0	0	0	;
26	1559.76	434.93	881.4439996	-431.3501824	1	100	1	1940	0	0	0	0	0	0	0	0	0	0	0	0	;
26	887.616	0	384.1098821	-294.6218936	1	100	1	1104	0	0	0	0	0	0	0	0	0	0	0	0	;
26	1981.86	0	1254.526922	-1114.638015	1	100	1	2465	0	0	0	0	0	0	0	0	0	0	0	0	;
26	0	0	0	0	1	100	1	100	0	0	0	0	0	0	0	0	0	0	0	0	;
27	869.928	416.22	666.0315259	-541.7921399	1	100	1	1082	0	0	0	0	0	0	0	0	0	0	0	0	;
27	173.664	0	71	0	1	100	1	216	0	0	0	0	0	0	0	0	0	0	0	0	;
28	1061.28	248.31	657.8243073	-579.7019351	1	100	1	1320	0	0	0	0	0	0	0	0	0	0	0	0	;
28	167.232	0	60.79357628	-71.20642372	1	100	1	208	0	0	0	0	0	0	0	0	0	0	0	0	;
29	1013.844	-480.42	455.3171992	-480.4288183	1	100	1	1261	0	0	0	0	0	0	0	0	0	0	0	0	;
29	727.62	-159.48	403.3543544	-412.0264373	1	100	1	905	0	0	0	0	0	0	0	0	0	0	0	0	;
29	727.62	-159.48	403.3543544	-412.0264373	1	100	1	905	0	0	0	0	0	0	0	0	0	0	0	0	; % Added G
29	0	0	0	0	1	100	1	100	0	0	0	0	0	0	0	0	0	0	0	0	;
1	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
2	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
3	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
4	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
5	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
6	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
7	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
8	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
9	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
10	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
11	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
12	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
13	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
14	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
15	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
16	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
17	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
18	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
19	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
20	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
21	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
22	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
23	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
24	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
25	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
26	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
27	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
28	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
29	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
30	0	0	10000	-10000	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
29	727.62	-159.48	403.3543544	-412.0264373	1	100	1	905	0	0	0	0	0	0	0	0	0	0	0	0	;
10	1507.5	0	697.1712682	-829.6266854	1	100	1	1875	0	0	0	0	0	0	0	0	0	0	0	0	;
1	12.83285	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; %   2020 update
2	22.14601	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
3	0	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
4	20.26	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
5	0	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
6	56.45480	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
7	0	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
8	37.22788	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
9	358.7428	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
10	0	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
11	223.5091	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
12	0	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
13	0	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
14	330.0236	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
15	88.54476	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
16	447.4752	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
17	341.7294	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
18	314.106	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
19	1235.928	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
20	558.764	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
21	199.8798	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
22	131.2619	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
23	380.3545	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
24	137.3883	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
25	604.3018    0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
26	299.3149	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
27	158.1385	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
28	406.027     0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
29	0	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
30	0	0	0	0	1	100	1	100000	0	0	0	0	0	0	0	0	0	0	0	0	; % 
];																						
																
										

%% generator cost data										
%	1	startup	shutdown	n	x1	y1	...	xn	yn	
%	2	startup	shutdown	n	c(n-1)	...	c0			
mpc.gencost = [										%
2	0	0	2	0	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	70	0	;			%
2	0	0	2	70	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	69.76	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	70	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	46	0	;			%
2	0	0	2	70	0	;			%
2	0	0	2	69.76	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	70	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	46	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	46	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	46	0	;			%
2	0	0	2	69.76	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	69.76	0	;			%
2	0	0	2	70	0	;			%
2	0	0	2	46	0	;			%
2	0	0	2	46	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	69.76	0	;			%
2	0	0	2	46	0	;			%
2	0	0	2	46	0	;			%
2	0	0	2	69.76	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	70	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	70	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	46	0	;			%
2	0	0	2	46	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	60	0	;			%
2	0	0	2	46	0	;			%
2	0	0	2	46	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	60	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	69.76	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	53.66	0	;			%
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200 0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	200	0	;			
2	0	0	2	201	0;
2	0	0	2	201	0;
2	0	0	2	53.66	0	;			%
2	0	0	2	8.05	0	;			%
2	0	0	2	0	0	;			% 2020
2	0	0	2	0	0	;			%
2	0	0	2	70	0	;			%
2	0	0	2	70	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	69.76	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	70	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	46	0	;			%
2	0	0	2	70	0	;			%
2	0	0	2	69.76	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	70	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	46	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	38.05	0	;			%
2	0	0	2	46	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	0	0	;			%
2	0	0	2	46	0	;			%
2	0	0	2	46	0	;			%
];										

%% Additional information

% Coordinates for each bus in the network
mpc.coordinates = [
    57.3333 -4.2740;57.3333 -1.9395;56.6900 -3.7072;55.9995 -3.4722;...
    55.9011 -4.3148;55.4788 -3.6556;55.7901 -2.4592;55.4925 -2.2516;...
    54.7987 -2.9623;54.8496 -1.7682;53.7369 -2.7327;53.2270 -3.3480;...
    53.3024 -2.2713;53.3024 -1.2386;53.7369 -0.9915;53.3546 -0.8158;...
    52.8028 -1.2606;52.2694 -1.9911;52.6860 0.2656;52.0274 1.0745;...
    51.9507 -0.1076;52.0227 -0.7897;51.4758 -2.2963;51.3848 -1.1349;...
    51.5527 -0.3406;51.4494 0.5145;51.1382 0.8878;50.9426 -1.1349;...
    50.9556 -2.3978;57.3333 -4.2740
    ];

%Demand profiles for every bus. The example is for 24 hours, but other time
%horizons and resolutions can be used. The idea is to pass this file with
%mpc data and, afterwards, just passing mpc.demand

%The information can be passed as a pu profile, which can then be used to
%scale the demand in all buses
mpc.demand = [
    0.5272 0.5521 0.5076 0.4580 0.4224 0.4059 0.4369 0.4927 0.5804 ...
    0.6698 0.7147 0.7312 0.7464 0.6920 0.6365 0.6475 0.7496 0.8689 ...
    0.8854 0.8421 0.7675 0.7148 0.6274 0.5115
    ];

%This is equivalent to producing the PQ data series below. The information
%can also be passed using the matrices below
mpc.demandP = [
 246.7296  258.3828  237.5568  214.3440  197.6832  189.9612  204.4692  230.5836  271.6272  313.4664  334.4796  342.2016  349.3152  323.8560  297.8820  303.0300  350.8128  406.6452  414.3672  394.1028  359.1900  334.5264  293.6232  239.3820 
 270.4536  283.2273  260.3988  234.9540  216.6912  208.2267  224.1297  252.7551  297.7452  343.6074  366.6411  375.1056  382.9032  354.9960  326.5245  332.1675  384.5448  445.7457  454.2102  431.9973  393.7275  366.6924  321.8562  262.3995 
 292.5960  306.4155  281.7180  254.1900  234.4320  225.2745  242.4795  273.4485  322.1220  371.7390  396.6585  405.8160  414.2520  384.0600  353.2575  359.3625  416.0280  482.2395  491.3970  467.3655  425.9625  396.7140  348.2070  283.8825 
 689.5776  722.1468  663.9408  599.0640  552.4992  530.9172  571.4652  644.4516  759.1632  876.0984  934.8276  956.4096  976.2912  905.1360  832.5420  846.9300  980.4768 1136.5212 1158.1032 1101.4668 1003.8900  934.9584  820.6392  669.0420 
 264.6544  277.1542  254.8152  229.9160  212.0448  203.7618  219.3238  247.3354  291.3608  336.2396  358.7794  367.0624  374.6928  347.3840  319.5230  325.0450  376.2992  436.1878  444.4708  422.7342  385.2850  358.8296  314.9548  256.7730 
 619.9872  649.2696  596.9376  538.6080  496.7424  477.3384  513.7944  579.4152  682.5504  787.6848  840.4872  859.8912  877.7664  813.7920  748.5240  761.4600  881.5296 1021.8264 1041.2304  990.3096  902.5800  840.6048  737.8224  601.5240 
 392.7640  411.3145  378.1620  341.2100  314.6880  302.3955  325.4905  367.0615  432.3980  499.0010  532.4515  544.7440  556.0680  515.5400  474.1925  482.3875  558.4520  647.3305  659.6230  627.3645  571.7875  532.5260  467.4130  381.0675 
 527.2000  552.1000  507.6000  458.0000  422.4000  405.9000  436.9000  492.7000  580.4000  669.8000  714.7000  731.2000  746.4000  692.0000  636.5000  647.5000  749.6000  868.9000  885.4000  842.1000  767.5000  714.8000  627.4000  511.5000 
  68.5360   71.7730   65.9880   59.5400   54.9120   52.7670   56.7970   64.0510   75.4520   87.0740   92.9110   95.0560   97.0320   89.9600   82.7450   84.1750   97.4480  112.9570  115.1020  109.4730   99.7750   92.9240   81.5620   66.4950 
1350.1592 1413.9281 1299.9636 1172.9380 1081.7664 1039.5099 1118.9009 1261.8047 1486.4044 1715.3578 1830.3467 1872.6032 1911.5304 1772.2120 1630.0765 1658.2475 1919.7256 2225.2529 2267.5094 2156.6181 1965.5675 1830.6028 1606.7714 1309.9515 
1771.3920 1855.0560 1705.5360 1538.8800 1419.2640 1363.8240 1467.9840 1655.4720 1950.1440 2250.5280 2401.3920 2456.8320 2507.9040 2325.1200 2138.6400 2175.6000 2518.6560 2919.5040 2974.9440 2829.4560 2578.8000 2401.7280 2108.0640 1718.6400 
 626.8408  656.4469  603.5364  544.5620  502.2336  482.6151  519.4741  585.8203  690.0956  796.3922  849.7783  869.3968  887.4696  822.7880  756.7985  769.8775  891.2744 1033.1221 1052.7406 1001.2569  912.5575  849.8972  745.9786  608.1735 
1330.6528 1393.5004 1281.1824 1155.9920 1066.1376 1024.4916 1102.7356 1243.5748 1464.9296 1690.5752 1803.9028 1845.5488 1883.9136 1746.6080 1606.5260 1634.2900 1891.9904 2193.1036 2234.7496 2125.4604 1937.1700 1804.1552 1583.5576 1291.0260 
 965.3032 1010.8951  929.4156  838.5980  773.4144  743.2029  799.9639  902.1337 1062.7124 1226.4038 1308.6157 1338.8272 1366.6584 1267.0520 1165.4315 1185.5725 1372.5176 1590.9559 1621.1674 1541.8851 1405.2925 1308.7988 1148.7694  936.5565 
1388.1176 1453.6793 1336.5108 1205.9140 1112.1792 1068.7347 1150.3577 1297.2791 1528.1932 1763.5834 1881.8051 1925.2496 1965.2712 1822.0360 1675.9045 1704.8675 1973.6968 2287.8137 2331.2582 2217.2493 2020.8275 1882.0684 1651.9442 1346.7795 
 847.2104  887.2247  815.7132  736.0060  678.7968  652.2813  702.0983  791.7689  932.7028 1076.3686 1148.5229 1175.0384 1199.4648 1112.0440 1022.8555 1040.5325 1204.6072 1396.3223 1422.8378 1353.2547 1233.3725 1148.6836 1008.2318  821.9805 
 569.9032  596.8201  548.7156  495.0980  456.6144  438.7779  472.2889  532.6087  627.4124  724.0538  772.5907  790.4272  806.8584  748.0520  688.0565  699.9475  810.3176  939.2809  957.1174  910.3101  829.6675  772.6988  678.2194  552.9315 
2826.8464 2960.3602 2721.7512 2455.7960 2264.9088 2176.4358 2342.6578 2641.8574 3112.1048 3591.4676 3832.2214 3920.6944 4002.1968 3710.5040 3412.9130 3471.8950 4019.3552 4659.0418 4747.5148 4515.3402 4115.3350 3832.7576 3364.1188 2742.6630 
1064.4168 1114.6899 1024.8444  924.7020  852.8256  819.5121  882.1011  994.7613 1171.8276 1352.3262 1442.9793 1476.2928 1506.9816 1397.1480 1285.0935 1307.3025 1513.4424 1754.3091 1787.6226 1700.1999 1549.5825 1443.1812 1266.7206 1032.7185 
 541.6242  567.2055  521.4879  470.5309  433.9569  417.0054  448.8536  506.1803  596.2797  688.1257  734.2542  751.2056  766.8215  710.9331  653.9146  665.2156  770.1091  892.6731  909.6245  865.1399  788.4988  734.3569  644.5657  525.4946 
 370.0944  387.5742  356.3352  321.5160  296.5248  284.9418  306.7038  345.8754  407.4408  470.1996  501.7194  513.3024  523.9728  485.7840  446.8230  454.5450  526.2192  609.9678  621.5508  591.1542  538.7850  501.7896  440.4348  359.0730 
 959.5040 1004.8220  923.8320  833.5600  768.7680  738.7380  795.1580  896.7140 1056.3280 1219.0360 1300.7540 1330.7840 1358.4480 1259.4400 1158.4300 1178.4500 1364.2720 1581.3980 1611.4280 1532.6220 1396.8500 1300.9360 1141.8680  930.9300 
2495.7648 2613.6414 2402.9784 2168.1720 1999.6416 1921.5306 2068.2846 2332.4418 2747.6136 3170.8332 3383.3898 3461.5008 3533.4576 3275.9280 3013.1910 3065.2650 3548.6064 4113.3726 4191.4836 3986.5014 3633.3450 3383.8632 2970.1116 2421.4410 
 747.5696  782.8778  719.7768  649.4440  598.9632  575.5662  619.5242  698.6486  823.0072  949.7764 1013.4446 1036.8416 1058.3952  981.2560  902.5570  918.1550 1062.9328 1232.1002 1255.4972 1194.0978 1088.3150 1013.5864  889.6532  725.3070 
5131.7648 5374.1414 4940.9784 4458.1720 4111.6416 3951.0306 4252.7846 4795.9418 5649.6136 6519.8332 6956.8898 7117.5008 7265.4576 6735.9280 6195.6910 6302.7650 7296.6064 8457.8726 8618.4836 8197.0014 7470.8450 6957.8632 6107.1116 4978.9410 
 750.7328  786.1904  722.8224  652.1920  601.4976  578.0016  622.1456  701.6048  826.4896  953.7952 1017.7328 1041.2288 1062.8736  985.4080  906.3760  922.0400 1067.4304 1237.3136 1260.8096 1199.1504 1092.9200 1017.8752  893.4176  728.3760 
 240.9304  252.3097  231.9732  209.3060  193.0368  185.4963  199.6633  225.1639  265.2428  306.0986  326.6179  334.1584  341.1048  316.2440  290.8805  295.9075  342.5672  397.0873  404.6278  384.8397  350.7475  326.6636  286.7218  233.7555 
1450.3272 1518.8271 1396.4076 1259.9580 1162.0224 1116.6309 1201.9119 1355.4177 1596.6804 1842.6198 1966.1397 2011.5312 2053.3464 1903.6920 1751.0115 1781.2725 2062.1496 2390.3439 2435.7354 2316.6171 2111.3925 1966.4148 1725.9774 1407.1365 
1358.5944 1422.7617 1308.0852 1180.2660 1088.5248 1046.0043 1125.8913 1269.6879 1495.6908 1726.0746 1841.7819 1884.3024 1923.4728 1783.2840 1640.2605 1668.6075 1931.7192 2239.1553 2281.6758 2170.0917 1977.8475 1842.0396 1616.8098 1318.1355 
0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000 
    ];
mpc.demandQ = [
  53.7744   56.3142   51.7752   46.7160   43.0848   41.4018   44.5638   50.2554   59.2008   68.3196   72.8994   74.5824   76.1328   70.5840   64.9230   66.0450   76.4592   88.6278   90.3108   85.8942   78.2850   72.9096   63.9948   52.1730 
  59.5736   62.3873   57.3588   51.7540   47.7312   45.8667   49.3697   55.6751   65.5852   75.6874   80.7611   82.6256   84.3432   78.1960   71.9245   73.1675   84.7048   98.1857  100.0502   95.1573   86.7275   80.7724   70.8962   57.7995 
  55.3560   57.9705   53.2980   48.0900   44.3520   42.6195   45.8745   51.7335   60.9420   70.3290   75.0435   76.7760   78.3720   72.6600   66.8325   67.9875   78.7080   91.2345   92.9670   88.4205   80.5875   75.0540   65.8770   53.7075 
 167.1224  175.0157  160.9092  145.1860  133.9008  128.6703  138.4973  156.1859  183.9868  212.3266  226.5599  231.7904  236.6088  219.3640  201.7705  205.2575  237.6232  275.4413  280.6718  266.9457  243.2975  226.5916  198.8858  162.1455 
  67.4816   70.6688   64.9728   58.6240   54.0672   51.9552   55.9232   63.0656   74.2912   85.7344   91.4816   93.5936   95.5392   88.5760   81.4720   82.8800   95.9488  111.2192  113.3312  107.7888   98.2400   91.4944   80.3072   65.4720 
 166.0680  173.9115  159.8940  144.2700  133.0560  127.8585  137.6235  155.2005  182.8260  210.9870  225.1305  230.3280  235.1160  217.9800  200.4975  203.9625  236.1240  273.7035  278.9010  265.2615  241.7625  225.1620  197.6310  161.1225 
  90.1512   94.4091   86.7996   78.3180   72.2304   69.4089   74.7099   84.2517   99.2484  114.5358  122.2137  125.0352  127.6344  118.3320  108.8415  110.7225  128.1816  148.5819  151.4034  143.9991  131.2425  122.2308  107.2854   87.4665 
  19.7173   20.6485   18.9842   17.1292   15.7978   15.1807   16.3401   18.4270   21.7070   25.0505   26.7298   27.3469   27.9154   25.8808   23.8051   24.2165   28.0350   32.4969   33.1140   31.4945   28.7045   26.7335   23.4648   19.1301 
  27.9416   29.2613   26.9028   24.2740   22.3872   21.5127   23.1557   26.1131   30.7612   35.4994   37.8791   38.7536   39.5592   36.6760   33.7345   34.3175   39.7288   46.0517   46.9262   44.6313   40.6775   37.8844   33.2522   27.1095 
 245.1480  256.7265  236.0340  212.9700  196.4160  188.7435  203.1585  229.1055  269.8860  311.4570  332.3355  340.0080  347.0760  321.7800  295.9725  301.0875  348.5640  404.0385  411.7110  391.5765  356.8875  332.3820  291.7410  237.8475 
 400.6720  419.5960  385.7760  348.0800  321.0240  308.4840  332.0440  374.4520  441.1040  509.0480  543.1720  555.7120  567.2640  525.9200  483.7400  492.1000  569.6960  660.3640  672.9040  639.9960  583.3000  543.2480  476.8240  388.7400 
 178.1936  186.6098  171.5688  154.8040  142.7712  137.1942  147.6722  166.5326  196.1752  226.3924  241.5686  247.1456  252.2832  233.8960  215.1370  218.8550  253.3648  293.6882  299.2652  284.6298  259.4150  241.6024  212.0612  172.8870 
 403.8352  422.9086  388.8216  350.8280  323.5584  310.9194  334.6654  377.4082  444.5864  513.0668  547.4602  560.0992  571.7424  530.0720  487.5590  495.9850  574.1936  665.5774  678.2164  645.0486  587.9050  547.5368  480.5884  391.8090 
 298.6588  312.7647  287.5554  259.4570  239.2896  229.9423  247.5038  279.1146  328.7966  379.4417  404.8775  414.2248  422.8356  392.0180  360.5772  366.8087  424.6484  492.2319  501.5791  477.0496  434.7887  404.9342  355.4221  289.7647 
 366.1931  383.4887  352.5790  318.1268  293.3990  281.9381  303.4707  342.2294  403.1458  465.2431  496.4306  507.8915  518.4494  480.6632  442.1129  449.7535  520.6722  603.5379  614.9988  584.9227  533.1055  496.5001  435.7920  355.2879 
 345.3160  361.6255  332.4780  299.9900  276.6720  265.8645  286.1695  322.7185  380.1620  438.7190  468.1285  478.9360  488.8920  453.2600  416.9075  424.1125  490.9880  569.1295  579.9370  551.5755  502.7125  468.1940  410.9470  335.0325 
 195.5912  204.8291  188.3196  169.9180  156.7104  150.5889  162.0899  182.7917  215.3284  248.4958  265.1537  271.2752  276.9144  256.7320  236.1415  240.2225  278.1016  322.3619  328.4834  312.4191  284.7425  265.1908  232.7654  189.7665 
1020.1320 1068.3135  982.2060  886.2300  817.3440  785.4165  845.4015  953.3745 1123.0740 1296.0630 1382.9445 1414.8720 1444.2840 1339.0200 1231.6275 1252.9125 1450.4760 1681.3215 1713.2490 1629.4635 1485.1125 1383.1380 1214.0190  989.7525 
 341.6256  357.7608  328.9248  296.7840  273.7152  263.0232  283.1112  319.2696  376.0992  434.0304  463.1256  473.8176  483.6672  448.4160  412.4520  419.5800  485.7408  563.0472  573.7392  545.6808  497.3400  463.1904  406.5552  331.4520 
 161.2178  168.8322  155.2241  140.0564  129.1699  124.1242  133.6040  150.6677  177.4863  204.8248  218.5553  223.6010  228.2491  211.6136  194.6417  198.0055  229.2277  265.7096  270.7553  257.5142  234.7015  218.5858  191.8589  156.4167 
 106.5998  111.6346  102.6367   92.6076   85.4093   82.0730   88.3412   99.6239  117.3569  135.4336  144.5123  147.8486  150.9221  139.9224  128.7003  130.9245  151.5691  175.6916  179.0279  170.2726  155.1885  144.5326  126.8603  103.4253 
 350.5880  367.1465  337.5540  304.5700  280.8960  269.9235  290.5385  327.6455  385.9660  445.4170  475.2755  486.2480  496.3560  460.1800  423.2725  430.5875  498.4840  577.8185  588.7910  559.9965  510.3875  475.3420  417.2210  340.1475 
 704.8664  738.1577  678.6612  612.3460  564.7488  542.6883  584.1353  658.7399  775.9948  895.5226  955.5539  977.6144  997.9368  925.2040  851.0005  865.7075 1002.2152 1161.7193 1183.7798 1125.8877 1026.1475  955.6876  838.8338  683.8755 
 278.3616  291.5088  268.0128  241.8240  223.0272  214.3152  230.6832  260.1456  306.4512  353.6544  377.3616  386.0736  394.0992  365.3760  336.0720  341.8800  395.7888  458.7792  467.4912  444.6288  405.2400  377.4144  331.2672  270.0720 
1529.9344 1602.1942 1473.0552 1329.1160 1225.8048 1177.9218 1267.8838 1429.8154 1684.3208 1943.7596 2074.0594 2121.9424 2166.0528 2008.1840 1847.1230 1879.0450 2175.3392 2521.5478 2569.4308 2443.7742 2227.2850 2074.3496 1820.7148 1484.3730 
 228.8048  239.6114  220.2984  198.7720  183.3216  176.1606  189.6146  213.8318  251.8936  290.6932  310.1798  317.3408  323.9376  300.3280  276.2410  281.0150  325.3264  377.1026  384.2636  365.4714  333.0950  310.2232  272.2916  221.9910 
  72.7536   76.1898   70.0488   63.2040   58.2912   56.0142   60.2922   67.9926   80.0952   92.4324   98.6286  100.9056  103.0032   95.4960   87.8370   89.3550  103.4448  119.9082  122.1852  116.2098  105.9150   98.6424   86.5812   70.5870 
 443.3752  464.3161  426.8916  385.1780  355.2384  341.3619  367.4329  414.3607  488.1164  563.3018  601.0627  614.9392  627.7224  581.9720  535.2965  544.5475  630.4136  730.7449  744.6214  708.2061  645.4675  601.1468  527.6434  430.1715 
 187.6832  196.5476  180.7056  163.0480  150.3744  144.5004  155.5364  175.4012  206.6224  238.4488  254.4332  260.3072  265.7184  246.3520  226.5940  230.5100  266.8576  309.3284  315.2024  299.7876  273.2300  254.4688  223.3544  182.0940 
   0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000    0.0000
    ];
