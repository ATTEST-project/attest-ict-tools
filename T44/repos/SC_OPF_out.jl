using XLSX#, DataFrames
function out_put_to_excel()
while true
if    empty_contin==1
    break
end


# We need to round the result for better understanding
PG=round.(value.(Pg), digits=3)
QG=round.(value.(Qg), digits=3)

LSH=round.(value.(pen_lsh), digits=3 )
WS=round.(value.(pen_ws), digits=3 )

XLSX.openxlsx("$(output_files_prefix)_Normal.xlsx", mode="w") do xf
# First of all set the first sheet name
    XLSX.rename!(xf[1], "Active_power")

#xf[1] menas the first sheet
    xf[1]["A1"] = "Gen_nodes"
    xf[1]["A2", dim=1]= bus_data_gsheet

    Pg_vect = Vector()
    for t in 1:nTP
        push!(Pg_vect,PG[t,:] )
    end
    labels=["t$t" for t in 1:nTP]

    XLSX.writetable!(xf[1], Pg_vect, labels, anchor_cell=XLSX.CellRef("B1"))
#---------------------------------------------------------------------
    XLSX.addsheet!(xf, "Reactive_Power")

#xf[1] menas the first sheet
    xf[2]["A1"] = "Gen_nodes"
    xf[2]["A2", dim=1]= bus_data_gsheet

    Qg_vect = Vector()
    for t in 1:nTP
        push!(Qg_vect,QG[t,:] )
    end
    labels=["t$t" for t in 1:nTP]

    XLSX.writetable!(xf[2], Qg_vect, labels, anchor_cell=XLSX.CellRef("B1"))
#--------------------------------------------------------------------

     XLSX.addsheet!(xf, "FL_inc")
     xf[3]["A1"] = "Flex_nodes"

     XLSX.addsheet!(xf, "FL_dec")
     xf[4]["A1"] = "Flex_nodes"

     if nFl!=0
         FL_inc=round.(value.(p_fl_inc), digits=3)
         FL_dec=round.(value.(p_fl_dec), digits=3)
     xf[3]["A2", dim=1]= nd_fl
        Fl_vect_inc = Vector()
          for t in 1:nTP
           push!(Fl_vect_inc,FL_inc[t,:] )
           end
    XLSX.writetable!(xf[3], Fl_vect_inc, labels, anchor_cell=XLSX.CellRef("B1"))


    xf[4]["A2", dim=1]= nd_fl
       Fl_vect_dec = Vector()
         for t in 1:nTP
          push!(Fl_vect_dec,FL_dec[t,:] )
          end
   XLSX.writetable!(xf[4], Fl_vect_dec, labels, anchor_cell=XLSX.CellRef("B1"))

      end
      XLSX.addsheet!(xf, "STR")
      xf[5]["A1"] = "STR_nodes"

      if nStr_active!=0

          STR=round.((value.(p_ch)-value.(p_dis)), digits=3)
          # STR=round.(STR, digits=3)




          xf[5]["A2", dim=1]= nd_Str_active
             STR_vect = Vector()
               for t in 1:nTP
                push!(STR_vect,STR[t,:] )
                end
         XLSX.writetable!(xf[5], STR_vect, labels, anchor_cell=XLSX.CellRef("B1"))
     end

     XLSX.addsheet!(xf, "Load_curtailment")
     xf[6]["A1"] = "Load_nodes"
     xf[6]["A2", dim=1]= bus_data_lsheet
        lsh_vect = Vector()
          for t in 1:nTP
           push!(lsh_vect,LSH[t,:] )
           end
    XLSX.writetable!(xf[6], lsh_vect, labels, anchor_cell=XLSX.CellRef("B1"))
# if !isempty(RES_bus)
    XLSX.addsheet!(xf, "RES_curtailment")
    xf[7]["A1"] = "RES_nodes"
    xf[7]["A2", dim=1]= RES_bus
       ws_vect = Vector()
         for t in 1:nTP
          push!(ws_vect,WS[t,:] )
          end
   XLSX.writetable!(xf[7], ws_vect, labels, anchor_cell=XLSX.CellRef("B1"))
# end
   XLSX.addsheet!(xf, "COSTS")
   xf[8]["A1"] = "Geereation Cost"
   xf[8]["B1"] = round.(value.(cost_gen), digits=3)
if  nFl!=0
   xf[8]["A2"] = "Flexibility Cost"
   xf[8]["B2"] = round.(value.(cost_fl), digits=3)
end
if nStr_active!=0
   xf[8]["A3"] = "Storage Cost"
   xf[8]["B3"] = round.(value.(cost_str), digits=3)
end
   xf[8]["A4"] = "Load curt. Cost"
   xf[8]["B4"] = round.(value.(cost_pen_lsh), digits=3)
if !isempty(RES_bus)
   xf[8]["A5"] = "RES curt. Cost"
   xf[8]["B5"] = round.(value.(cost_pen_ws), digits=3)
end
   xf[8]["A6"] = "Total Cost"
   xf[8]["B6"] = round.(JuMP.objective_value(model_name), digits=3)

   xf[8]["A7"] = "Elapsed time "
   xf[8]["B7"] = round.(JuMP.solve_time(model_name), digits=3)




end


##===============Post contingency====ACTIVE POWER====
XLSX.openxlsx("$(output_files_prefix)_PContin_ActiveP.xlsx", mode="w") do xf
PG_C=round.(value.(Pg_c), digits=3)
# QG_C=round.(value.(Qg_c), digits=3)
#
# LSH_C=round.(value.(pen_lsh_c), digits=3 )
# WS_C=round.(value.(pen_ws_c), digits=3 )
XLSX.rename!(xf[1], "Active_power")
xf[1]["A1"] = "Number of Contingencies"
xf[1]["B1"] = nCont

xf[1]["A2"] = "Number of Scenarios"
xf[1]["B2"] = nSc


for c in 1:nCont, s in 1:nSc
    XLSX.addsheet!(xf, "Active_power_Contin_$(c)_Scen_$(s)")

    xf[c+s]["A1"] = "Gen_nodes"
    xf[c+s]["A2", dim=1]= bus_data_gsheet

    Pgc_vect = Vector()
    for t in 1:nTP
        push!(Pgc_vect,PG_C[c,s,t,:] )
    end
    labels=["t$t" for t in 1:nTP]

    XLSX.writetable!(xf[c+s], Pgc_vect, labels, anchor_cell=XLSX.CellRef("B1"))
end
end

##===============Post contingency====REACTIVE POWER====
XLSX.openxlsx("$(output_files_prefix)_PContin_ReactiveP.xlsx", mode="w") do xf

# PG_C=round.(value.(Pg_c), digits=3)
QG_C=round.(value.(Qg_c), digits=3)

# LSH_C=round.(value.(pen_lsh_c), digits=3 )
# WS_C=round.(value.(pen_ws_c), digits=3 )
XLSX.rename!(xf[1], "Rective_power")
xf[1]["A1"] = "Number of Contingencies"
xf[1]["B1"] = nCont

xf[1]["A2"] = "Number of Scenarios"
xf[1]["B2"] = nSc


for c in 1:nCont, s in 1:nSc
    XLSX.addsheet!(xf, "Reactive_power_Contin_$(c)_Scen_$(s)")

    xf[c+s]["A1"] = "Gen_nodes"
    xf[c+s]["A2", dim=1]= bus_data_gsheet

    Qgc_vect = Vector()
    for t in 1:nTP
        push!(Qgc_vect,QG_C[c,s,t,:] )
    end
    labels=["t$t" for t in 1:nTP]

    XLSX.writetable!(xf[c+s], Qgc_vect, labels, anchor_cell=XLSX.CellRef("B1"))
end
end

##===============Post contingency====FL inc====
XLSX.openxlsx("$(output_files_prefix)_PContin_FL_inc.xlsx", mode="w") do xf
XLSX.rename!(xf[1], "Flexible_Load")
xf[1]["A1"] = "Number of Fleaxible Loads"
if nFl==0
      xf[1]["B1"] = "No flexible load"
  else
      FL_inc_c=round.(value.(p_fl_inc_c), digits=3)
      # FL_dec_c=round.(value.(p_fl_dec_c), digits=3)
  xf[1]["B1"] = nFl
  for c in 1:nCont, s in 1:nSc
    XLSX.addsheet!(xf, "FL_inc_Contin_$(c)_Scen_$(s)")

    xf[c+s]["A1"] = "FL_nodes"
    xf[c+s]["A2", dim=1]= nd_fl

    FL_inc_vect = Vector()
    for t in 1:nTP
        push!(FL_inc_vect,FL_inc_c[c,s,t,:] )
    end
    labels=["t$t" for t in 1:nTP]

    XLSX.writetable!(xf[c+s], FL_inc_vect, labels, anchor_cell=XLSX.CellRef("B1"))
   end


end
end

##===============Post contingency====FL dec====

XLSX.openxlsx("$(output_files_prefix)_PContin_FL_dec.xlsx", mode="w") do xf
XLSX.rename!(xf[1], "Flexible_Load")
xf[1]["A1"] = "Number of Fleaxible Loads"
if nFl==0
      xf[1]["B1"] = "No flexible load"
  else
      # FL_inc_c=round.(value.(p_fl_inc_c), digits=3)
      FL_dec_c=round.(value.(p_fl_dec_c), digits=3)
  xf[1]["B1"] = nFl
  for c in 1:nCont, s in 1:nSc
    XLSX.addsheet!(xf, "FL_dec_Contin_$(c)_Scen_$(s)")

    xf[c+s]["A1"] = "FL_nodes"
    xf[c+s]["A2", dim=1]= nd_fl

    FL_dec_vect = Vector()
    for t in 1:nTP
        push!(FL_dec_vect,FL_dec_c[c,s,t,:] )
    end
    labels=["t$t" for t in 1:nTP]

    XLSX.writetable!(xf[c+s], FL_dec_vect, labels, anchor_cell=XLSX.CellRef("B1"))
   end


end
end


##===============Post contingency====STR====

XLSX.openxlsx("$(output_files_prefix)_PContin_STR.xlsx", mode="w") do xf
XLSX.rename!(xf[1], "Storage")
xf[1]["A1"] = "Number of Storages"
if nStr_active==0
      xf[1]["B1"] = "No Storage"
  else
 STR=round.((value.(p_ch_c)-value.(p_dis_c)), digits=3)

  xf[1]["B1"] = nStr_active
  for c in 1:nCont, s in 1:nSc
    XLSX.addsheet!(xf, "STR_Contin_$(c)_Scen_$(s)")

    xf[c+s]["A1"] = "STR_nodes"
    xf[c+s]["A2", dim=1]= nd_Str_active

    STR_vect = Vector()
    for t in 1:nTP
        push!(STR_vect,STR[c,s,t,:] )
    end
    labels=["t$t" for t in 1:nTP]

    XLSX.writetable!(xf[c+s], STR_vect, labels, anchor_cell=XLSX.CellRef("B1"))
   end


end
end

##===============Post contingency====Load curtailment ====

XLSX.openxlsx("$(output_files_prefix)_PContin_LC.xlsx", mode="w") do xf
XLSX.rename!(xf[1], "LC")
xf[1]["A1"] = "Number of Contingencies"
xf[1]["B1"] = nCont

xf[1]["A2"] = "Number of Scenarios"
xf[1]["B2"] = nSc
LSH_C=round.((value.(pen_lsh_c)), digits=3)

  for c in 1:nCont, s in 1:nSc
    XLSX.addsheet!(xf, "LC_Contin_$(c)_Scen_$(s)")

    xf[c+s]["A1"] = "LC_nodes"
    xf[c+s]["A2", dim=1]= bus_data_lsheet

    LSH_vect = Vector()
    for t in 1:nTP
        push!(LSH_vect,LSH_C[c,s,t,:] )
    end
    labels=["t$t" for t in 1:nTP]

    XLSX.writetable!(xf[c+s], LSH_vect, labels, anchor_cell=XLSX.CellRef("B1"))
   end



end

##===============Post contingency====RES curtailment ====

XLSX.openxlsx("$(output_files_prefix)_PContin_RES_C.xlsx", mode="w") do xf
XLSX.rename!(xf[1], "RES")
xf[1]["A1"] = "Number of Contingencies"
xf[1]["B1"] = nCont

xf[1]["A2"] = "Number of Scenarios"
xf[1]["B2"] = nSc
WS_C=round.((value.(pen_ws_c)), digits=3)

  for c in 1:nCont, s in 1:nSc
    XLSX.addsheet!(xf, "RES_C_Contin_$(c)_Scen_$(s)")

    xf[c+s]["A1"] = "RES_nodes"
    xf[c+s]["A2", dim=1]= RES_bus

    WS_C_vect = Vector()
    for t in 1:nTP
        push!(WS_C_vect,WS_C[c,s,t,:] )
    end
    labels=["t$t" for t in 1:nTP]

    XLSX.writetable!(xf[c+s], WS_C_vect, labels, anchor_cell=XLSX.CellRef("B1"))
   end



end

##=============Post contingency costs===
XLSX.openxlsx("$(output_files_prefix)_Costs.xlsx", mode="w") do xf

    xf[1]["A1"] = "Geereation Cost"
    xf[1]["B1"] = round.(value.(cost_gen), digits=3)
    xf[1]["C1"] = "Probability of Normal operation is 95% and 5% all of the post contingency states."
  if  nFl!=0
    xf[1]["A2"] = "Flexibility Cost"
    xf[1]["B2"] = round.(value.(cost_fl), digits=3)
  end
  if nStr_active!=0
    xf[1]["A3"] = "Storage Cost"
    xf[1]["B3"] = round.(value.(cost_str), digits=3)
  end

    xf[1]["A4"] = "Load curt. Cost"
    if value.(cost_pen_lsh)[1]<0
    xf[1]["B4"] = 0
    else
    xf[1]["B4"] = round.(value.(cost_pen_lsh), digits=3)
    end
  if !isempty(RES_bus)
    xf[1]["A5"] = "RES curt. Cost"
    if value.(cost_pen_ws)[1]<0
    xf[1]["B5"] =0
    else
    xf[1]["B5"] = round.(value.(cost_pen_ws), digits=3)
    end
  end
xf[1]["A6"] = "Post contingency costs"
xf[1]["C6"] = "Scenarios are equiprobable."
if  nFl!=0
xf[1]["A7"] = "Flexibility Cost"
xf[1]["B7"] = round.(value.(cost_fl_c), digits=3)
end
if nStr_active!=0
xf[1]["A8"] = "Storage Cost"
xf[1]["B8"] = round.(value.(cost_str_c), digits=3)
end
xf[1]["A9"] = "Load curt. Cost"
 if value.(cost_pen_lsh_c)[1]<0
xf[1]["B9"] = 0
else
xf[1]["B9"] = round.(value.(cost_pen_lsh_c), digits=3)
end
if !isempty(RES_bus)
xf[1]["A10"] = "RES curt. Cost"
if value.(cost_pen_ws_c)[1]<0
xf[1]["B10"] = 0
else
xf[1]["B10"] = round.(value.(cost_pen_ws_c), digits=3)
end
end

xf[1]["A11"] = "Total Cost"
xf[1]["B11"] = round.(JuMP.objective_value(model_name), digits=3)

xf[1]["A12"] = "Elapsed time "
xf[1]["B12"] = round.(JuMP.solve_time(model_name), digits=3)
end

break
end
end
out_put_to_excel()
