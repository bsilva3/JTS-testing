//This file is part of SECONDO.

//Copyright (C) 2014, University in Hagen, Department of Computer Science,
//Database Systems for New Applications.

//SECONDO is free software; you can redistribute it and/or modify
//it under the terms of the GNU General Public License as published by
//the Free Software Foundation; either version 2 of the License, or
//(at your option) any later version.

//SECONDO is distributed in the hope that it will be useful,
//but WITHOUT ANY WARRANTY; without even the implied warranty of
//MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//GNU General Public License for more details.

//You should have received a copy of the GNU General Public License
//along with SECONDO; if not, write to the Free Software
//Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

package mmdb.gui.query;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.util.ArrayList;
import java.util.List;
import java.util.Vector;

import javax.swing.BorderFactory;
import javax.swing.BoxLayout;
import javax.swing.ButtonGroup;
import javax.swing.DefaultComboBoxModel;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JScrollPane;
import javax.swing.ListSelectionModel;
import javax.swing.ScrollPaneConstants;
import javax.swing.SwingConstants;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;

import mmdb.MMDBUserInterfaceController;
import mmdb.data.MemoryRelation;
import mmdb.data.RelationHeaderItem;
import mmdb.data.attributes.MemoryAttribute;
import mmdb.error.memory.MemoryException;
import mmdb.error.query.QueryException;
import mmdb.gui.QueryDialog;
import mmdb.operator.OperationController;
import mmdb.operator.OperationController.COperator;
import tools.Reporter;

/**
 * The panel representing the 'JOIN' query.
 *
 * @author Alexander Castor
 */
public class JoinPanel extends AbstractOperationPanel {

	private static final long serialVersionUID = -6679479531695801670L;

	/**
	 * The height of the bottom area.
	 */
	private static final int BOTTOM_AREA_HEIGHT = 140;

	/**
	 * The first list of relations which can be joined.
	 */
	private JList firstRelationList;

	/**
	 * The second list of relations which can be joined.
	 */
	private JList secondRelationList;

	/**
	 * The list of operations that can be selected.
	 */
	private JComboBox operatorList;

	/**
	 * The list of join attributes from the first relation.
	 */
	private JComboBox firstJoinAttributeList;

	/**
	 * The list of join attributes from the second relation.
	 */
	private JComboBox secondJoinAttributeList;

	/**
	 * The previously selected value from the second attribute list.
	 */
	private String previousValueSelection;

	/**
	 * The radio button for query mode selection.
	 */
	private JRadioButton queryModeNormal;

	/*
	 * (non-Javadoc)
	 * 
	 * @see mmdb.gui.operation.AbstractOperationPanel#constructPanel()
	 */
	@Override
	public void constructPanel() {
		this.setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
		addDescriptionPanel("MERGE THE ATTRIBUTES OF TWO GIVEN RELATIONS DEPENDING ON A CONDITION",
				this);
		createLists();
		JPanel topArea = new JPanel(new GridLayout(1, 2));
		topArea.setPreferredSize(new Dimension(QueryDialog.DIALOG_WIDTH, MIDDLE_HEIGHT
				- BOTTOM_AREA_HEIGHT));
		addRelationPanel(firstRelationList, firstJoinAttributeList, "1) FIRST RELATION", topArea);
		addRelationPanel(secondRelationList, secondJoinAttributeList, "2) SECOND RELATION", topArea);
		this.add(topArea);
		JPanel bottomArea = new JPanel(new GridLayout(2, 1));
		bottomArea.setPreferredSize(new Dimension(QueryDialog.DIALOG_WIDTH, BOTTOM_AREA_HEIGHT));
		JPanel topBottomArea = new JPanel(new GridLayout(1, 2));
		addOperatorPanel(topBottomArea);
		addModePanel(topBottomArea);
		bottomArea.add(topBottomArea);
		JPanel bottomBottomArea = new JPanel(new GridLayout(1, 2));
		addAttributePanels(bottomBottomArea);
		bottomArea.add(bottomBottomArea);
		this.add(bottomArea);
		addConvertToListPanel(this);
		addButtonPanel(this);
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see mmdb.gui.query.AbstractOperationPanel#createButtonListener()
	 */
	@Override
	protected ActionListener createButtonListener() {
		return new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent event) {
				if (operatorList.getSelectedItem() == null
						|| firstJoinAttributeList.getSelectedItem() == null
						|| secondJoinAttributeList.getSelectedItem() == null
						|| firstRelationList.getSelectedValue() == null
						|| secondRelationList.getSelectedValue() == null) {
					Reporter.showInfo("Please select relations, attributes and operator.");
					return;
				}
				COperator selectedOperator = (COperator) operatorList.getSelectedItem();
				String firstSelectedAttribute = (String) firstJoinAttributeList.getSelectedItem();
				String secondSelectedAttribute = (String) secondJoinAttributeList.getSelectedItem();
				if (selectedOperator.parameterTypesEqual
						&& !removeIdentifier(firstSelectedAttribute).equals(
								removeIdentifier(secondSelectedAttribute))) {
					Reporter.showInfo("Selected attributes do not match.");
					return;
				}
				MemoryRelation resultRelation = null;
				String firstSelectedRelation = (String) firstRelationList.getSelectedValue();
				String secondSelectedRelation = (String) secondRelationList.getSelectedValue();
				boolean normalQuery = queryModeNormal.isSelected();
				long startTime = System.currentTimeMillis();
				try {
					resultRelation = queryController.executeQuery(
							relations.get(firstSelectedRelation),
							relations.get(secondSelectedRelation),
							removeType(firstSelectedAttribute),
							removeType(secondSelectedAttribute), selectedOperator, normalQuery);
				} catch (QueryException e) {
					Throwable unexpected = e.getUnexpectedError();
					if (unexpected != null) {
						unexpected.printStackTrace();
						Reporter.showError("Unexpected error occured during join operation.\n"
								+ "See console for details.");
					} else {
						Reporter.showWarning(e.getMessage());
					}
					return;
				} catch (MemoryException e) {
					dialog.dispose();
					MMDBUserInterfaceController.getInstance().processMemoryException(e);
				}
				long endTime = System.currentTimeMillis();
				if (normalQuery) {
					answer[0] = resultRelation;
					answer[1] = createObjectName("JOIN", firstSelectedRelation,
							secondSelectedRelation);
					answer[2] = convert.isSelected();
					dialog.setVisible(false);
					dialog.dispose();
				} else {
					showMeasureModeInfoBox(resultRelation, endTime - startTime);
				}
			}
		};
	}

	/**
	 * Initializes the relation and attribute lists.
	 */
	private void createLists() {
		Vector<String> vector = new Vector<String>(relations.keySet());
		firstRelationList = new JList(vector);
		secondRelationList = new JList(vector);
		firstJoinAttributeList = new JComboBox(new DefaultComboBoxModel());
		secondJoinAttributeList = new JComboBox(new DefaultComboBoxModel());
	}

	/**
	 * Adds the relation selection panel to the underlying container.
	 * 
	 * @param relationList
	 *            the list of relations
	 * @param attributeList
	 *            the list of attributes
	 * @param title
	 *            the component's title
	 * @param area
	 *            the underlying container the components are added to
	 */
	private void addRelationPanel(final JList relationList, final JComboBox attributeList,
			final String title, JPanel area) {
		relationList.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		relationList.addListSelectionListener(new ListSelectionListener() {
			@Override
			public void valueChanged(ListSelectionEvent e) {
				if (title.contains("FIRST")) {
					fillCondAttributeList((String) relationList.getSelectedValue(),
							(COperator) operatorList.getSelectedItem(), attributeList);
				} else {
					fillCondValueList();
				}
			}
		});
		JScrollPane relationSelectionPane = new JScrollPane(relationList,
				ScrollPaneConstants.VERTICAL_SCROLLBAR_AS_NEEDED,
				ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
		relationSelectionPane.setBorder(BorderFactory.createTitledBorder(title));
		relationSelectionPane.setPreferredSize(new Dimension(QueryDialog.DIALOG_WIDTH / 2,
				MIDDLE_HEIGHT - BOTTOM_AREA_HEIGHT));
		area.add(relationSelectionPane);
	}

	/**
	 * Adds the operator panel to the underlying container.
	 * 
	 * @param area
	 *            the underlying container the components are added to
	 */
	private void addOperatorPanel(JPanel area) {
		JPanel operationPanel = new JPanel(new FlowLayout());
		operationPanel.setBorder(BorderFactory.createTitledBorder("3) OPERATOR"));
		operatorList = new JComboBox(COperator.values());
		((JLabel) operatorList.getRenderer()).setHorizontalAlignment(SwingConstants.CENTER);
		operatorList.setSelectedItem(null);
		operatorList.setPreferredSize(new Dimension(200, 30));
		operatorList.addItemListener(new ItemListener() {
			@Override
			public void itemStateChanged(ItemEvent e) {
				fillCondAttributeList((String) firstRelationList.getSelectedValue(),
						(COperator) operatorList.getSelectedItem(), firstJoinAttributeList);
				// fillCondValueList();
			}
		});
		operationPanel.add(operatorList);
		operationPanel.setBackground(Color.WHITE);
		area.add(operationPanel);
	}

	/**
	 * Adds the mode panel to the underlying container.
	 * 
	 * @param area
	 *            the underlying container the components are added to
	 */
	private void addModePanel(JPanel area) {
		JPanel modeArea = new JPanel(new FlowLayout(FlowLayout.CENTER, 30, 0));
		modeArea.setBorder(BorderFactory.createTitledBorder("4) QUERY-MODE"));
		queryModeNormal = new JRadioButton("normal");
		JRadioButton queryModeCount = new JRadioButton("measure");
		ButtonGroup group = new ButtonGroup();
		group.add(queryModeNormal);
		group.add(queryModeCount);
		queryModeNormal.setSelected(true);
		queryModeNormal.setPreferredSize(new Dimension(85, 30));
		queryModeCount.setPreferredSize(new Dimension(85, 30));
		modeArea.add(queryModeNormal);
		modeArea.add(queryModeCount);
		modeArea.setBackground(Color.WHITE);
		area.setBackground(Color.WHITE);
		area.add(modeArea);
	}

	/**
	 * Adds the attribute panel to the underlying container.
	 * 
	 * @param area
	 *            the underlying container the components are added to
	 */
	private void addAttributePanels(JPanel area) {
		JPanel attributePanelFirst = new JPanel(new FlowLayout());
		attributePanelFirst.setBorder(BorderFactory
				.createTitledBorder("5) ATTRIBUTE - FIRST RELATION"));
		firstJoinAttributeList.setPreferredSize(new Dimension(200, 30));
		firstJoinAttributeList.addItemListener(new ItemListener() {
			@Override
			public void itemStateChanged(ItemEvent e) {
				fillCondValueList();
			}
		});
		((JLabel) firstJoinAttributeList.getRenderer())
				.setHorizontalAlignment(SwingConstants.CENTER);
		attributePanelFirst.add(firstJoinAttributeList);
		attributePanelFirst.setBackground(Color.WHITE);
		JPanel attributePanelSecond = new JPanel(new FlowLayout());
		attributePanelSecond.setBorder(BorderFactory
				.createTitledBorder("6) ATTRIBUTE - SECOND RELATION"));
		secondJoinAttributeList.setPreferredSize(new Dimension(200, 30));
		((JLabel) secondJoinAttributeList.getRenderer())
				.setHorizontalAlignment(SwingConstants.CENTER);
		attributePanelSecond.add(secondJoinAttributeList);
		attributePanelSecond.setBackground(Color.WHITE);
		area.add(attributePanelFirst);
		area.add(attributePanelSecond);
	}

	/**
	 * Dynamically fills a value attribute list for a conditional operator
	 * depending on the user's relation, operator and first argument selection.
	 */
	private void fillCondValueList() {
		if (secondJoinAttributeList.getSelectedItem() != null) {
			previousValueSelection = (String) secondJoinAttributeList.getSelectedItem();
		}
		DefaultComboBoxModel model = (DefaultComboBoxModel) secondJoinAttributeList.getModel();
		model.removeAllElements();
		String selectedRelation = (String) secondRelationList.getSelectedValue();
		String selectedFirstAttribute = (String) firstJoinAttributeList.getSelectedItem();
		COperator selectedOperator = (COperator) operatorList.getSelectedItem();
		if (selectedRelation == null || selectedOperator == null || selectedFirstAttribute == null) {
			return;
		}
		Class<? extends MemoryAttribute> attributeClass = MemoryAttribute
				.getTypeClass(removeIdentifier(selectedFirstAttribute));
		MemoryRelation relation = relations.get(selectedRelation);
		List<Class<?>> argumentClasses = OperationController.getCondValueClasses(selectedOperator,
				attributeClass);
		List<String> insertedElements = new ArrayList<String>();
		for (RelationHeaderItem item : relation.getHeader()) {
			if (!item.isProjected()) {
				continue;
			}
			for (Class<?> argumentClass : argumentClasses) {
				if (argumentClass.isAssignableFrom(item.getType())) {
					String element = item.getIdentifier() + " (" + item.getTypeName() + ")";
					if (selectedOperator.parameterTypesEqual
							&& !item.getTypeName().equals(removeIdentifier(selectedFirstAttribute))) {
						continue;
					}
					if (!insertedElements.contains(element)) {
						model.addElement(element);
						insertedElements.add(element);
					}
				}
			}
		}
		int previousIndex = model.getIndexOf(previousValueSelection);
		if (!insertedElements.isEmpty() && previousIndex > 0) {
			secondJoinAttributeList.setSelectedIndex(previousIndex);
		}
	}
}
