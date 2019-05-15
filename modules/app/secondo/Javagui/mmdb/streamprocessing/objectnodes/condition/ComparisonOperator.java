package mmdb.streamprocessing.objectnodes.condition;

import mmdb.data.MemoryObject;
import mmdb.data.MemoryObjects;
import mmdb.data.attributes.MemoryAttribute;
import mmdb.data.attributes.standard.AttributeBool;
import mmdb.error.streamprocessing.TypeException;
import mmdb.streamprocessing.Node;
import mmdb.streamprocessing.objectnodes.ObjectNode;
import mmdb.streamprocessing.tools.TypecheckTools;

/**
 * Abstract base class for comparison operators with two parameters.
 * 
 * @author Bjoern Clasen
 *
 */
public abstract class ComparisonOperator implements ObjectNode {

	/**
	 * The operator's parameter Nodes.
	 */
	protected Node input1, input2;

	/**
	 * The operators parameters as ObjectNodes.
	 */
	protected ObjectNode objectInput1, objectInput2;

	/**
	 * The operator's output type.
	 */
	protected MemoryAttribute outputType;

	/**
	 * Constructor, called by fromNL(...)
	 * 
	 * @param input1
	 *            operator's first parameter
	 * @param input2
	 *            operator's second parameter
	 */
	public ComparisonOperator(Node input1, Node input2) {
		this.input1 = input1;
		this.input2 = input2;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void typeCheck() throws TypeException {
		this.input1.typeCheck();
		this.input2.typeCheck();
		
		// Is input1 an ObjectNode?
		TypecheckTools.checkNodeType(this.input1, ObjectNode.class,
				this.getClass(), 1);
		this.objectInput1 = (ObjectNode) this.input1;

		// Is input2 an ObjectNode?
		TypecheckTools.checkNodeType(this.input2, ObjectNode.class,
				this.getClass(), 2);
		this.objectInput2 = (ObjectNode) this.input2;

		// Are both outputTypes the same?
		checkOutputTypesMatch();

		// Do both outputTypes implement comparable? (only check 1 since they do
		// match)
		TypecheckTools.checkOutputTypeHasIFace(this.input1, Comparable.class,
				this.getClass(), 1);

		this.outputType = new AttributeBool();
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public MemoryObject getOutputType() {
		return this.outputType;
	}

	/**
	 * Checks if the OutputTypes of the parameters match so they can be
	 * compared.
	 * 
	 * @throws TypeException
	 *             if the OutputTypes do not match.
	 */
	private void checkOutputTypesMatch() throws TypeException {
		Class<?> class1 = this.objectInput1.getOutputType().getClass();
		Class<?> class2 = this.objectInput2.getOutputType().getClass();
		if (class1 != class2) {
			throw new TypeException(
					"%s's inputs are of different types: %s != %s", this
							.getClass().getSimpleName(),
					MemoryObjects.getTypeName(class1),
					MemoryObjects.getTypeName(class2));
		}
	}

}
