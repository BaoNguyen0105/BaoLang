package baolang;

import java.util.ArrayList;
@SuppressWarnings("unchecked")
public class BaoLangOperators {
    public static Object add(Object left, Object right){
        if (left instanceof Integer && right instanceof Integer) {
            return (Integer)left + (Integer)right;
        } else if (left instanceof Float && right instanceof Float) {
            return (Float)left + (Float)right;
        } else if (left instanceof Integer && right instanceof Float) {
            return ((Integer)left).floatValue() + (Float)right;
        } else if (left instanceof Float && right instanceof Integer) {
            return (Float)left + ((Integer)right).floatValue();
        } else if (left instanceof String || right instanceof String) {
            return left.toString() + right.toString();
        } else if (left instanceof ArrayList && right instanceof ArrayList) {
            ArrayList<Object> result = new ArrayList<Object>();
            result.addAll((ArrayList<Object>)left);
            result.addAll((ArrayList<Object>)right);
            return result;
        } else {
            throw new UnsupportedOperationException("Addition not supported for given types");
        }
    }
    public static Object sub(Object left, Object right){
        if (left instanceof Integer && right instanceof Integer) {
            return (Integer)left - (Integer)right;
        } else if (left instanceof Float && right instanceof Float) {
            return (Float)left - (Float)right;
        } else if (left instanceof Integer && right instanceof Float) {
            return ((Integer)left).floatValue() - (Float)right;
        } else if (left instanceof Float && right instanceof Integer) {
            return (Float)left - ((Integer)right).floatValue();
        } else {
            throw new UnsupportedOperationException("Subtraction not supported for given types");
        }
    }
    public static Object mul(Object left, Object right){
        if (left instanceof Integer && right instanceof Integer) {
            return (Integer)left * (Integer)right;
        } else if (left instanceof Float && right instanceof Float) {
            return (Float)left * (Float)right;
        } else {
            throw new UnsupportedOperationException("Multiplication not supported for given types");
        }
    }
    public static Object div(Object left, Object right){
        if (left instanceof Integer && right instanceof Integer) {
            return (Integer)left / (Integer)right;
        } else if (left instanceof Float && right instanceof Float) {
            return (Float)left / (Float)right;
        } else {
            throw new UnsupportedOperationException("Division not supported for given types");
        }
    }
    public static Object mod(Object left, Object right){
        if (left instanceof Integer && right instanceof Integer) {
            return (Integer)left % (Integer)right;
        } else {
            throw new UnsupportedOperationException("Modulo not supported for given types");
        }
    }
    public static Object and(Object left, Object right){
        if (left instanceof Boolean && right instanceof Boolean) {
            return (Boolean)left && (Boolean)right;
        } else {
            throw new UnsupportedOperationException("Logical AND not supported for given types");
        }
    }
    public static Object or(Object left, Object right){
        if (left instanceof Boolean && right instanceof Boolean) {
            return (Boolean)left || (Boolean)right;
        } else {
            throw new UnsupportedOperationException("Logical OR not supported for given types");
        }
    }
    public static Object not(Object operand){
        if (operand instanceof Boolean) {
            return !(Boolean)operand;
        } else {
            throw new UnsupportedOperationException("Logical NOT not supported for given type");
        }
    }
    public static Object neg(Object operand){
        if (operand instanceof Integer) {
            return -(Integer)operand;
        } else if (operand instanceof Float) {
            return -(Float)operand;
        } else {
            throw new UnsupportedOperationException("Negation not supported for given type");
        }
    }
    public static Object eq(Object left, Object right){
        return left.equals(right);
    }
    public static Object ne(Object left, Object right){
        return !left.equals(right);
    }
    public static Object gt(Object left, Object right){
        if (left instanceof Integer && right instanceof Integer) {
            return (Integer)left > (Integer)right;
        } else if (left instanceof Float && right instanceof Float) {
            return (Float)left > (Float)right;
        } else {
            throw new UnsupportedOperationException("Greater than comparison not supported for given types");
        }
    }
    public static Object lt(Object left, Object right){
        if (left instanceof Integer && right instanceof Integer) {
            return (Integer)left < (Integer)right;
        } else if (left instanceof Float && right instanceof Float) {
            return (Float)left < (Float)right;
        } else {
            throw new UnsupportedOperationException("Less than comparison not supported for given types");
        }
    }
    public static Object ge(Object left, Object right){
        if (left instanceof Integer && right instanceof Integer) {
            return (Integer)left >= (Integer)right;
        } else if (left instanceof Float && right instanceof Float) {
            return (Float)left >= (Float)right;
        } else {
            throw new UnsupportedOperationException("Greater than or equal comparison not supported for given types");
        }
    }
    public static Object le(Object left, Object right){
        if (left instanceof Integer && right instanceof Integer) {
            return (Integer)left <= (Integer)right;
        } else if (left instanceof Float && right instanceof Float) {
            return (Float)left <= (Float)right;
        } else {
            throw new UnsupportedOperationException("Less than or equal comparison not supported for given types");
        }
    }
}


