#ifndef PID_PID_H
#define PID_PID_H

class PID {
public:
  PID(double, double, double);
  PID(double, double, double, double);
  double getP();
  double getI();
  double getD();
  double getF();
  void setP(double);
  void setI(double);
  void setD(double);
  void setF(double);
  void setPID(double, double, double);
  void setPID(double, double, double, double);
  void setMaxIOutput(double);
  void setOutputLimits(double);
  void setOutputLimits(double,double);
  void setDirection(bool);
  void setSetpoint(double);
  void reset();
  void setOutputRampRate(double);
  void setSetpointRange(double);
  void setOutputFilter(double);
  void setDeadBandWindow(double);
  double getOutput();
  double getOutput(double);
  double getOutput(double, double);

private:
  double clamp(double, double, double);
  bool bounded(double, double, double);
  void checkSigns();
  void init();
  double P;
  double I;
  double D;
  double F;

  double maxIOutput;
  double maxError;
  double errorSum;

  double maxOutput;
  double minOutput;

  double setpoint;

  double lastActual;

  bool firstRun;
  bool reversed;

  double outputRampRate;
  double lastOutput;

  double outputFilter;

  double setpointRange;

  double deadBandWindow;
};

#endif
