package baolang;

import java.util.ArrayList;
@SuppressWarnings("unchecked")
public class BaoLangFunctions {
    public static Object toint(Object operand){
        if (operand instanceof Float) {
            return ((Float)operand).intValue();
        } else if (operand instanceof String) {
            return Integer.parseInt((String)operand);
        } else {
            throw new UnsupportedOperationException("Conversion to int not supported for given type");
        }
    }
    public static Object tofloat(Object operand){
        if (operand instanceof Integer) {
            return ((Integer)operand).floatValue();
        } else if (operand instanceof String) {
            return Float.parseFloat((String)operand);
        } else {
            throw new UnsupportedOperationException("Conversion to float not supported for given type");
        }
    }
    public static Object tostring(Object operand){
        return operand.toString();
    }
    public static Object toboolean(Object operand){
        if (operand instanceof Integer) {
            return (Integer)operand != 0;
        } else if (operand instanceof Float) {
            return (Float)operand != 0.0f;
        } else if (operand instanceof String) {
            return !((String)operand).isEmpty();
        } else {
            throw new UnsupportedOperationException("Conversion to boolean not supported for given type");
        }
    }
    public static Object print(Object operand){
        System.out.println(operand);
        return operand;
    }
    public static Object reduce(Object func, Object list, Object initial){
        Object result = initial;
        for (Object item : (ArrayList<Object>)list) {
            ArrayList<Object> temp = new ArrayList<Object>();
            temp.add(result);
            temp.add(item);
            result = ((LambdaInterface)func).call(temp);
        }
        return result;
    }
    public static Object map(Object func, Object list){
        ArrayList<Object> result = new ArrayList<Object>();
        for (Object item : (ArrayList<Object>)list) {
            ArrayList<Object> temp = new ArrayList<Object>();
            temp.add(item);
            result.add(((LambdaInterface)func).call(temp));
        }
        return result;
    }
    public static Object filter(Object func, Object list){
        ArrayList<Object> result = new ArrayList<Object>();
        for (Object item : (ArrayList<Object>)list) {
            ArrayList<Object> temp = new ArrayList<Object>();
            temp.add(item);
            if ((Boolean)((LambdaInterface)func).call(temp)) {
                result.add(item);
            }
        }
        return result;
    }
}

