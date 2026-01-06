.source Lambda0.java
.class public Lambda0
.super java/lang/Object
.implements baolang/LambdaInterface

.method public <init>()V
Label0:
.var 0 is this Ljava/lang/Object; from Label0 to Label1
	aload_0
	invokespecial java/lang/Object/<init>()V
	return
Label1:
.limit stack 1
.limit locals 1
.end method

.method public call(Ljava/util/ArrayList;)Ljava/lang/Object;
Label0:
.var 0 is this Ljava/lang/Object; from Label0 to Label1
.var 1 is args Ljava/lang/Object; from Label0 to Label1
	aload_1
	iconst_0
	invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
	checkcast java/lang/Integer
	invokevirtual java/lang/Integer/intValue()I
	invokevirtual java/util/ArrayList/get(I)Ljava/lang/Object;
.var 2 is x Ljava/lang/Object; from Label0 to Label1
	astore_2
	aload_1
	iconst_1
	invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
	checkcast java/lang/Integer
	invokevirtual java/lang/Integer/intValue()I
	invokevirtual java/util/ArrayList/get(I)Ljava/lang/Object;
.var 3 is y Ljava/lang/Object; from Label0 to Label1
	astore_3
	aload_2
	aload_3
	invokestatic baolang/BaoLangOperators/add(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
	areturn
Label1:
.limit stack 9
.limit locals 4
.end method
