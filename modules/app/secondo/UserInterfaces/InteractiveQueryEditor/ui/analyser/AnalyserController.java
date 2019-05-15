//This file is part of SECONDO.

//Copyright (C) 2004, University in Hagen, Department of Computer Science,
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

package ui.analyser;

import javax.swing.JFrame;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;

import ui.InteractiveQueryEditorController;
import util.common.QueryAnalyser;
import util.common.SearchField;
import util.domain.EditorEvent;
import util.domain.EditorEventListener;
import util.exceptionhandling.ExceptionHandler;

/**
 * The controller handels all the UI events of the {@link AnalyserPanel}
 * @author D.Merle
 */
public class AnalyserController implements DocumentListener, EditorEventListener {
	private final JFrame parent;
	private final QueryAnalyser analyser;
	private final AnalyserModel model;

	/**
	 * The constructor initializes the {@link QueryAnalyser}
	 * @param parent
	 * @param model
	 */
	public AnalyserController(final JFrame parent, final AnalyserModel model) {
		this.parent = parent;
		this.model = model;
		analyser = new QueryAnalyser("../Algebras/specs");
	}

	/**
	 * This method handles all {@link EditorEvent}s fired by the {@link InteractiveQueryEditorController}
	 */
	@Override
	public void handleEditorEvent(final EditorEvent event) {
		if (event.getEventType().equals(EditorEvent.INIT_DB_CONNECTION)) {
			model.setDBConnectionStatus(true);
			model.setAnalyserStatusMessage(model.getNoTypeMessage());
			model.notifyDataUpdate();
		} else if (event.getEventType().equals(EditorEvent.COMMAND_UPDATED)) {
			final String command = event.getCommand();
			if (model.isDBConnectionInitialized()) {
				if (command.startsWith("query ") && command.length() > 6) {
					String typeInformation = "";
					try {
						typeInformation = analyser.analyseQuery(command);
					} catch (final Exception e) {
						ExceptionHandler.showException(parent, e, "");
					}
					model.setTypeInformation(typeInformation);
					model.setLastValidTypeInformation(typeInformation);
				} else{
					model.setTypeInformation(null);
					model.setLastValidTypeInformation(null);
				}
				model.notifyDataUpdate();
			}
		} else if (event.getEventType().equals(EditorEvent.CLOSE_DB_CONNECTION)) {
			model.setDBConnectionStatus(false);
			model.setAnalyserStatusMessage(model.getStartMessage());
			model.notifyDataUpdate();
		} else if (event.getEventType().equals(EditorEvent.NEW_COMMAND)) {
			model.setTypeInformation(null);
			model.setLastValidTypeInformation(null);
			model.notifyDataUpdate();
		}
	}

	/**
	 * This method notifies the {@link AnalyserModel} about changes to the Document of the {@link SearchField}.
	 */
	@Override
	public void insertUpdate(final DocumentEvent e) {
		model.updateHighlighting();
	}

	/**
	 * This method notifies the {@link AnalyserModel} about changes to the Document of the {@link SearchField}.
	 */
	@Override
	public void removeUpdate(final DocumentEvent e) {
		model.updateHighlighting();
	}

	/**
	 * This method notifies the {@link AnalyserModel} about changes to the Document of the {@link SearchField}.
	 */
	@Override
	public void changedUpdate(final DocumentEvent e) {
		model.updateHighlighting();
	}
}