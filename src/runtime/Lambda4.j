.source Lambda4.java
.class public Lambda4
.super java/lang/Object
.implements baolang/LambdaInterface
.field x Ljava/lang/Object;

.method public <init>(Ljava/lang/Object;)V
Label0:
.var 0 is this Ljava/lang/Object; from Label0 to Label1
	aload_0
	invokespecial java/lang/Object/<init>()V
.var 1 is x Ljava/lang/Object; from Label0 to Label1
	aload_0
	aload_1
	putfield Lambda4/x Ljava/lang/Object;
	return
Label1:
.limit stack 3
.limit locals 2
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
.var 2 is y Ljava/lang/Object; from Label0 to Label1
	astore_2
	new Lambda5
	dup
	aload_0
	getfield Lambda4/x Ljava/lang/Object;
	aload_2
	invokespecial Lambda5/<init>(Ljava/lang/Object;Ljava/lang/Object;)V
	areturn
Label1:
.limit stack 8
.limit locals 3
.end method
