echo "Ax,Ay,Az,Hx,Hy,Hz,Vx,Vy,Vz,H0x,H0y,H0z,V0x,V0y,V0z" > voodoo_result_v1.csv
cat voodoo_raw_result_v1.txt | grep -v "#" | awk '{ print $3","$4","$5","$6","$7","$8","$9","$10","$11","$23","$24","$25","$26","$27","$28 }' >> voodoo_result_v1.csv
